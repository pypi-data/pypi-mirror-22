#!/usr/bin/env hy
(import
  [os]
  [re]
  [json]
  [datetime [datetime]]
  [urllib2 [urlopen]] 
  [bs4 [BeautifulSoup]])

(require [hy.contrib.loop [loop]])

(def urls
 {:search "https://github.com/search?utf8=%%E2%%9C%%93&q=user%%3A%s+fork%%3Atrue&type=Repositories&ref=advsearch"
  :home "https://github.com/%s"
  :repos "https://api.github.com/users/%s/repos?per_page=1000"})

(defn usage [args]
  (+ "Usage: " (get args 0) " [--contributions|--stats] github-username\n"
     "\t--contributions will print the SVG contributions graph to stdout.\n"
     "\t--stats will print JSON formatted statistics for the user to stdout.\n"
     "\t--repos will print JSON formatted list of user's public repos."))

(defn fetch [url username]
  (->> username
       (% url)
       (urlopen)))

(defn scrape-github-page [url username]
  (BeautifulSoup
    (->
      (fetch url username)
      (.read))
    "html.parser"))

(defn extract-digits [string]
  (int (.join "" (list-comp c [c string] (if (in c "0123456789"))))))

(defn dict-merge [d1 d2] (apply dict [d1] (or d2 {})))

(defn command-contributions [username]
  (let [user-page (scrape-github-page (get urls :home) username)]
    (user-page.find :class "js-calendar-graph-svg")))

(defn stat-int-element [s t]
  (let [result
        (-> s (.find :href (fn [e] (and e (.endswith e t)))))]
    (if result
      (int (or (first (re.findall "\d+" result.text)) 0))
      0)))

(defn fetch-stats [username]
  (let [user-page (scrape-github-page (get urls :home) username)
        stats-page (scrape-github-page (get urls :search) username)]
    {"timestamp" (-> (datetime.now) (.isoformat))
     "contributions-year" (-> user-page (.find :class "js-contribution-graph") (. h2) (. string) (extract-digits))
     "stats" (list-comp (-> (. stat text) (.replace " " "") (.split "\n") (cut 1 -2 2)) [stat (-> user-page (.find-all :class "underline-nav-item"))] (stat.find :class "Counter"))
     "pinned-repos" (list-comp {"name" (-> stat (.find :class "js-repo") (. text))
                                "url" (+ "https://github.com" (-> stat (.find "a" :class "text-bold") (get "href")))
                                "description" (-> stat (.find :class "pinned-repo-desc") (. text))
                                "language" (-> stat (.find :class "repo-language-color") (. next_sibling) (.replace " " "") (.replace "\n" ""))
                                "stars" (stat-int-element stat "stargazers")
                                "forks" (stat-int-element stat "network")}
                               [stat (-> user-page (.find-all :class "pinned-repo-item"))])
     "languages" (list-comp {"language" (-> language (.find :class "filter-item") (. text) (.replace " " "") (.split "\n") (get 2))
                             "percent" (-> language (.find :class "bar") (get "style") (extract-digits))
                             "count" (-> language (.find :class "count") (. text) (int))}
                            [language (-> stats-page (.find :class "filter-list") (.find-all "li"))])}))

(defn command-stats [username]
  (json.dumps (fetch-stats username) :indent 2))

(defn repos-keep-keys [repos]
  (list-comp
    (dict-comp
      k (get r k)
      [k r]
      (in k ["id"
             "stargazers_count"
             "watchers_count"
             "updated_at"
             "created_at"
             "full_name"
             "name"
             "description"
             "html_url"
             "size"
             "language"
             "fork"
             "forks_count"
             "forks"
             "open_issues_count"
             "open_issues"
             "watchers_count"
             "watchers"
             "clone_url"
             "ssh_url"]))
    [r repos]))

(defn next-link [request]
  (first (list-comp (re.sub ".*<(.*)>; rel=\"next\".*" "\\1" h)
                    [h (. (request.info) headers)]
                    (and
                      (.startswith h "Link")
                      (re.search "; rel=\"next\"" h)))))

(defn fetch-repos [username &optional [url None]]
  (let [request (if url
                  (urlopen url)
                  (fetch (get urls :repos) username))
        repos (-> (request.read)
                  (json.loads)
                  (repos-keep-keys))
        repos-next-link (next-link request)]
    (->
      (if repos-next-link
        (+ repos (fetch-repos username :url repos-next-link))
        repos)
      (sorted :key (fn [r] (,
                            (get r "stargazers_count")
                            (get r "watchers_count")
                            (get r "updated_at")
                            (get r "created_at")))
              :reverse True))))

(defn command-repos [username]
  (-> (fetch-repos username)
      (json.dumps :indent 2)))

(defn scrape [command username]
  (cond [(= command "--contributions") (print (command-contributions username))]
        [(= command "--stats") (print (command-stats username))]
        [(= command "--repos") (print (command-repos username))]
        [True (print "Unknown command" command)]))

(defn main [args]
  (try
    (if (< (len args) 3)
      (print (usage args))
      (apply scrape (cut args 1 3)))
    (except [e Exception]
            (print "Oops:" (str e)))))

(defmain [&rest args]
  (main args))
