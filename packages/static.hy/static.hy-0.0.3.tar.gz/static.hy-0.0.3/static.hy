#!/usr/bin/env hy3

(import
  [glob [glob]]
  [re [compile]]
  [json [load dump JSONEncoder]]
  [os.path [exists]]
  [jinja2 [Template]]
  [markdown [Markdown]]
  [datetime [datetime]]
  [collections [defaultdict]]
)

(setv
  NOW (+ (cut (.isoformat (datetime.now)) 0 19) 'Z)
  CONFIG (load (open "config.json"))
  HIDDEN (.get CONFIG 'hide [])
  ROOT (get CONFIG 'home_page_url)
  HTML (.read (open "html.jinja2"))
  ATOM (.read (open "atom.jinja2"))
  TITLE (compile "<h1>([^<]+)</h1>")
  SUMMARY (compile "<p>([^<]+)</p>")
  FEED (dict
    :author (or (.get CONFIG 'author) {'name "Please set author in config.json"})
    :home_page_url (or (.strip (.get CONFIG 'home_page_url "") '/)
                      "Please set home_page_url in config.json")
    :title (or (.get CONFIG 'title) "Please set title in config.json")
    :description (or (.get CONFIG 'description) "Please set description in config.json")
    :version "https://jsonfeed.org/version/1"
    :user_comment "Confused? Please see https://jsonfeed.org"
    :feed_url (.format "{}/feed.json" ROOT)
    :_generated NOW
    :expired False
    :hubs []
    :items []
  )
)

(defclass JSONFilter [JSONEncoder]
  "An extension of JSONEncoder that can filter out dict keys."

  (defn iterencode [self o]
    (setv o_copy (.copy o))
    (.update o_copy :items (list-comp
      (dict-comp key val [(, key val) (.items item)] (not (in key HIDDEN)))
      (item (get o 'items))))
    (.iterencode (super) o_copy)
  )
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

(dump FEED (open 'feed.json 'w) :indent 2 :sort_keys True :cls JSONFilter)

(.update FEED :page {})
(.write (open 'index.html 'w) (.render (Template HTML) FEED))
(.write (open 'feed.atom  'w) (.render (Template ATOM) FEED))

(for [item (get FEED 'items)]
  (setv path (.replace (get item 'url) ROOT '.))
  (if (.endswith path '/) (setv path (+ path 'index.html)))
  (.update FEED :page item)
  (.write (open path 'w) (.render (Template HTML) FEED))
)
