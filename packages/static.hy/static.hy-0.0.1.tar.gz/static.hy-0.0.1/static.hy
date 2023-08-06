#!/usr/bin/env hy3

(import
  [glob [glob]]
  [re [compile]]
  [json [load dump]]
  [os.path [exists]]
  [jinja2 [Template]]
  [markdown [Markdown]]
  [datetime [datetime]]
  [collections [defaultdict]]
)

(setv
  NOW (+ (cut (.isoformat (datetime.now)) 0 19) 'Z)
  CONFIG (load (open "config.json"))
  ROOT (get CONFIG 'home_page_url)
  HTML (.read (open "html.jinja2"))
  ATOM (.read (open "atom.jinja2"))
  FEED (.copy CONFIG)
  TITLE (compile "<h1>([^<]+)</h1>")
  SUMMARY (compile "<p>([^<]+)</p>")
)

; TODO: Improve robustness with parsedate
(defn format-date [date]
  (if (= (len date) 10)
    (+ date "T12:00:00Z")
    date)
)

(defn first-match [regex string]
  (setv obj (.search regex string))
  (if obj (.group obj 1))
)

(.update FEED
  :version "https://jsonfeed.org/version/1"
  :user_comment "Confused? Please see https://jsonfeed.org"
  :feed_url (.format "{}/feed.json" ROOT)
  :_generated NOW
  :expired False
  :hubs []
  :items []
)

(for [path (sorted (glob "**/*.md" :recursive True))]
  (setv
    raw (.read (open path))
    output (.replace path '.md '.html)
    permalink (.replace output 'index.html "")
    url (.format "{}/{}" ROOT permalink)
    md (Markdown :extensions ["markdown.extensions.meta"])
    html (.convert md raw)
    meta (dict-comp key (get val -1) [(, key val) (.items md.Meta)])
    author (.get meta 'author)
    date (.get meta 'date NOW)
    item (dict
      :title (or (.get meta 'title) (first-match TITLE html) "")
      :summary (or (.get meta 'summary) (first-match SUMMARY html) "")
      :date_published (format-date (.get meta 'datepublished date))
      :date_modified (format-date (.get meta 'datemodified date))
      :content_html html
      :url url
      :id url
      :tags (.split (.replace (.get meta 'tags "") ', " "))
    )
  )
  (if author (.update item :author {'name author}))
  (.append (get FEED 'items) item)
)

(dump FEED (open 'feed.json 'w) :indent 2 :sort_keys True)

(.update FEED :page {})
(.write (open 'index.html 'w) (.render (Template HTML) FEED))
(.write (open 'feed.atom  'w) (.render (Template ATOM) FEED))

(for [item (get FEED 'items)]
  (setv path (.replace (get item 'url) ROOT '.))
  (if (.endswith path '/) (setv path (+ path 'index.html)))
  (.update FEED :page item)
  (.write (open path 'w) (.render (Template HTML) FEED))
)
