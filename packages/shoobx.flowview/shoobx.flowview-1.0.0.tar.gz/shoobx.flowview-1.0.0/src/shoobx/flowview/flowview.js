<script>
<![CDATA[

DEFAULT_URL = "http://localhost:8080";

function indexTags(tags) {
    var indexed = {};
    for (var i=0; i<tags.length; i++) {
        var item = tags[i];
        if (item.tag in indexed) {
            indexed[item.tag].items.push(item);
        }
        else {
            indexed[item.tag] = {items: [item]};
        }
    }
    return indexed;
}

function tokenize(text) {
    return text.split(/[^a-zA-Z0-9_-]+/);
}

/* Return sorted unique values of an array
 *
 * Stolen from http://stackoverflow.com/questions/1960473/unique-values-in-an-array
 */
function sortUnique(arr) {
    arr.sort();
    var last_i;
    for (var i=0;i<arr.length;i++)
        if ((last_i = arr.lastIndexOf(arr[i])) !== i)
            arr.splice(i+1, last_i-i);
    return arr;
}

/* finds the intersection of
 * two arrays in a simple fashion.
 *
 * PARAMS
 *  a - first array, must already be sorted
 *  b - second array, must already be sorted
 *
 * NOTES
 *
 *  Should have O(n) operations, where n is
 *    n = MIN(a.length(), b.length())
 *
 * Stolen from http://stackoverflow.com/questions/1885557/simplest-code-for-array-intersection-in-javascript
 */
function intersect(a, b)
{
    var ai=0, bi=0;
    var result = new Array();

    while( ai < a.length && bi < b.length )
    {
        if      (a[ai] < b[bi] ){ ai++; }
        else if (a[ai] > b[bi] ){ bi++; }
        else /* they're equal */
        {
            result.push(a[ai]);
            ai++;
            bi++;
        }
      }

  return result;
}

function makeTagLinkHtml(tag) {
    return "<a class='tag'>"+tag+"</a>";
}

function makeTagPopoverHtml(taginfo) {
    var contents = "";
    var baseurl = localStorage.baseurl;
    for (var i=0; i<taginfo.items.length; i++) {
        var item = taginfo.items[i];
        var absurl = baseurl + "/" + item.href;
        contents += "<li>";
        contents += "<i class='fa fa-" + item.icon + "'></i> ";
        contents += "<a target='flowview' href='" + absurl + "'>";
        contents += item.title + "</a>"
        contents += "</li>";
    }
    return contents;
}

function linkSource(e, indexedTags, sortedTags) {
    // Find tokens that can be replaced with links
    var tokens = sortUnique(tokenize(e.textContent));
    var common = intersect(tokens, sortedTags)

    if (common.length == 0) return;

    // Replace
    var textnodes =  $(e).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    });

    textnodes.each(function(idx, node) {
        newcontents = node.nodeValue;
        for (var i=0; i < common.length; i++) {
            var tag = common[i];
            var newcontents = newcontents.replace(
                new RegExp("\\b"+tag+"\\b", 'g'), makeTagLinkHtml(tag));
        }
        $(node).replaceWith($("<span>"+newcontents+"</span>"));
    });
}

function initPopover(e, indexedTags) {
    var $e = $(e);
    var tag = $e.text();

    // Format contents
    var taginfo = indexedTags[tag];

    $e.popover({
        html: true,
        title: "References for " + tag,
        placement: "auto",
        trigger: "manual",
        container: "body"
    }).click(function() {
        var contents = makeTagPopoverHtml(taginfo);
        $(this).addClass("tag-active");
        $(this).attr("data-content", "<ul class='tags'>" + contents + "</ul>");
        $(this).popover('toggle');
    });
}

function setupBaseUrl() {
    var baseUrlInput = $("#baseurl");
    var setBaseUrl = function(e) {
        console.log("SETTING");
        localStorage.baseurl = baseUrlInput.val();
        e.preventDefault();
        return false;
    }
    baseUrlInput.blur(setBaseUrl);
    baseUrlInput.closest("form").on("submit", function(e) {
        // Unfocus base url input (this will set new value)
        $(".navbar-brand").focus();
        e.preventDefault()
    });

    if (localStorage.baseurl == undefined) {
        localStorage.baseurl = DEFAULT_URL;
    }
    baseUrlInput.val(localStorage.baseurl);
}


$(function() {
    var indexed = indexTags(TAGS);
    var tags = Object.keys(indexed);
    tags.sort()
    $(".source").each(function(idx, e) {
        linkSource(e, indexed, tags);
    });

    $(".tag").each(function(idx, e) {
        initPopover(e, indexed);
    });

    setupBaseUrl();

    $('body').on('click', function (e) {
        $('.tag-active').each(function () {

            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).removeClass("tag-active");
                $(this).popover('hide');
            }
        });
    });
})

]]>
</script>