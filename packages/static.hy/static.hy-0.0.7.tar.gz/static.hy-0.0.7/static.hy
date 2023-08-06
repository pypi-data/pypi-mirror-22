#!/usr/bin/env hy3

(import
  [glob [glob]]
  [re [compile]]
  [json [load dump]]
  [os.path [exists]]
  [jinja2 [Template]]
  [markdown [Markdown]]
  [datetime [datetime]]
  [dateutil.parser [parse]]
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
  BY_TAG (defaultdict list)
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

(defn filter-dict [feed]
  "Allow users to suppress certain JSON Feed elements, such as content_html."
  (setv feed_copy (.copy feed))
  (.update feed_copy :items (list-comp
    (dict-comp key val [(, key val) (.items item)] (not (in key HIDDEN)))
    (item (get feed 'items))))
  feed_copy
)

(defn format-date [date]
  "Canonicalize the date formatting."
  (setv obj (parse date))
  (, (.strftime obj "%Y-%m-%dT%H:%M:%SZ")
     (.strftime obj (.get CONFIG 'date_format "%A, %B %e, %Y")))
)

(defn first-match [regex string]
  "Find the first regex match in a string."
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
    published (.get meta 'datepublished date)
    modified (.get meta 'datemodified date)
    item (dict
      :title (or (.get meta 'title) (first-match TITLE html) "")
      :summary (or (.get meta 'summary) (first-match SUMMARY html) "")
      :content_html html
      :url url
      :id url
      :tags (.split (.replace (.get meta 'tags "") ', " "))
    )
    (, (get item 'date_published) (get item '_display_date_published)) (format-date published)
    (, (get item 'date_modified)  (get item '_display_date_modified))  (format-date modified)
  )
  (if author (.update item :author {'name author}))
  (.append (get FEED 'items) item)
)

; Sort feed items by date_published
(.update FEED
  :items (sorted (get FEED 'items) :reverse True :key (lambda [item] (get item 'date_published)))
)

(for [item (get FEED 'items)]
  (for [tag (get item 'tags)]
    (.append (get BY_TAG tag) item)
  )
)

(dump (filter-dict FEED) (open 'feed.json 'w) :indent 2 :sort_keys True)

(.update FEED :page {} :items_by_tag BY_TAG)
(.write (open 'index.html 'w) (.render (Template HTML) FEED))
(.write (open 'feed.atom  'w) (.render (Template ATOM) FEED))

(for [item (get FEED 'items)]
  (setv path (.replace (get item 'url) ROOT '.))
  (if (.endswith path '/) (setv path (+ path 'index.html)))
  (.update FEED :page item)
  (.write (open path 'w) (.render (Template HTML) FEED))
)
