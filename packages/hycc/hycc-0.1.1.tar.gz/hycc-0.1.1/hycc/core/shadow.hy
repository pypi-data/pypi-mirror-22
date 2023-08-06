(defclass hycc-dict [dict]
  (defn --init-- [self &rest args &kwargs kwargs]
    (apply dict.--init-- (+ (tuple [self]) args) kwargs) self)

  (defn --getitem-- [self key]
    (try
     (get (dict self) key)
     (except [KeyError]
        (get (dict self) (.--mangle self key)))))

  (defn --mangle-bang [self name]
    (if (.endswith name "!")
      (.replace name "!" "_bang") name))

  (defn --mangle-is [self name]
    (if (.endswith name "?")
      (+ "is_" (get name (slice -1))) name))

  (defn --mangle-invalid-name [self name]
    (import [hycc.core.translate [mangle :as hycc-mangle]])
    (hycc-mangle name))

  (defn --mangle [self name]
    (->> name
        (.--mangle-bang self)
        (.--mangle-is self)
        (.--mangle-invalid-name self))))


(defmacro globals []
  (with-gensyms [globals dict retval]
    `(do
      (setv ~globals globals)
      (import [hycc.core.shadow [hycc-dict :as ~dict]])
      (setv ~retval (~dict (~globals)))
      ~retval)))

(defmacro locals []
  (with-gensyms [locals dict retval]
    `(do
      (setv ~locals locals)
      (import [hycc.core.shadow [hycc-dict :as ~dict]])
      (setv ~retval (~dict (~locals)))
      ~retval)))
