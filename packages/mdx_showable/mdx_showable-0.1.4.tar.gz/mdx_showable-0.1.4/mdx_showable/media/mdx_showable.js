function getUrlParam(p) {
    var u = window.location.search.substring(1);
    var v = u.split('&');
    for (var i = 0; i < v.length; i++) {
        var n = v[i].split('=');
        if (n[0] == p) {
	        if (n.length == 1)
	        	return true;
            return n[1];
        }
    }
    return false;
}

/**
 * If user provides "exp" GET variable then expand all showables. I.e. for development. 
 **/
if (getUrlParam("exp") !== false) {
	$(document).ready(function(){
		$('div.showable-header > a').click();
	});
}


/**
 * JQuery plugin (TODO: complete)
 * 
 *
<div class="showable-container answer" id="showable3">
	<div class="showable-inner">
		<div class="showable-header answer" id="showabletitle3">
			<a href="" id="showablelink3">Answer</a> &lt;- click here to reveal answer
		</div>
		<div class="showable-body answer" id="showablebody3">
			Content
		</div>
	</div>
</div>
 * 
 */
(function( $ ) {
 
    $.fn.showable = function() {
 
        this.filter( "a" ).each(function() {
            var link = $( this );
            link.append( " (" + link.attr( "href" ) + ")" );
        });
 
        return this;
 
    };
 
}( jQuery ));




