$(document).ready(function(){
    connect_more_less();
    
    function toggle(link)
    {
        id = link.attr('id');
        id = id.substr(10);
        
        $("div#description_"+id+" div.info_less").toggle();
        $("div#description_"+id+" div.info_more").toggle();
        
        return false;
    }
});
    
function connect_more_less()
{
    $("a.link_less").click(function(){return toggle($(this))});
    $("a.link_more").click(function(){return toggle($(this))});
}