

// Low-level utility method for select the text in a HTML dom element
function select_dom_element(element)
{
       // firefox
        if(document.createRange) {
                var rangeToSelect = document.createRange();
                rangeToSelect.selectNode(element.firstChild);
                var curSelect = window.getSelection();
                curSelect.addRange(rangeToSelect);
                //console.log(this.firstChild);
        }
        // ie
        if(document.body && document.body.createTextRange) {
                var range = document.body.createTextRange();
                range.moveToElementText(element);
                range.select();
        }
        return false;
}
