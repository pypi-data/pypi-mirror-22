
Setup for reveal.js
===================

::

    Reveal.initialize({
        width: 1076,
        height: 600,

        margin: 0.1,

        minScale: 0.2,
        maxScale: 1.0,

        controls: true,
        progress: true,
        history: false,
        center: true,

        keyboard : true,
        overview: true,
        touch: true,
        loop: false,
        rtl: false,
        fragments: true,

        autoSlide: 0,
        mouseWheel: true,
        rollingLinks: true,
        previewLinks: true,

        transitionSpeed: "default",
        backgroundTransition: "default",

        slideNumber: true,
        embedded: false,
        autoSlideStoppable: true,
        hideAddressBar: true,

        parallaxBackgroundImage: "",
        parallaxBackgroundSize: "",

        focusBodyOnPageVisiblityChange: true,

        viewDistance: 3,

        transition: Reveal.getQueryHash().transition || "linear",

        math: {
            mathjax: "http://cdn.mathjax.org/mathjax/latest/MathJax.js",config: "TeX-AMS_HTML-full"},

        dependencies: [
           { src: '_static/lib/js/classList.js', condition: function() { return !document.body.classList; } },
           { src: '_static/plugin/markdown/marked.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
           { src: '_static/plugin/markdown/markdown.js', condition: function() { return !!document.querySelector( '[data-markdown]' ); } },
           { src: '_static/plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
           { src: '_static/plugin/zoom-js/zoom.js', async: true, condition: function() { return !!document.body.classList; } },
           { src: '_static/plugin/leap/leap.js', async: true, condition: function() { return !!document.body.classList; } },

           { src: '_static/plugin/multiplex/master.js', async: true, condition: function() { return !!document.body.classList; } },

           { src: '_static/plugin/remotes/remotes.js_static/plugin/notes-server/client.js', async: true, condition: function() { return !!document.body.classList; } },

           { src: '_static/plugin/math/math.js', async: true, condition: function() { return !!document.body.classList; } },

           { src: '_static/plugin/notes/notes.js', async: true, condition: function() { return !!document.body.classList; } }
        ]
      });
