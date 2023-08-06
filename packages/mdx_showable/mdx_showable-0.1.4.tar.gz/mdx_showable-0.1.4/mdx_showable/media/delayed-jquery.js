/* Processes delayed jquery commands after it is loaded */
/* @see http://writing.colin-gourlay.com/safely-using-ready-before-including-jquery/ */
(function($,d,w){if(w._delayed){$.each(readyQ,function(i,f){$(f);});$.each(bindReadyQ,function(i,f){$(d).bind("ready",f);});console.info("Delayed JQuery executed");}})(jQuery,document,window);
