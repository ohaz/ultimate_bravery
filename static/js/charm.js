function showCharm(id){
    var charms = [$("#maxspells-charm").data("charm"), $("#items-charm").data("charm"), $("#link-charm").data("charm")];
    var charm = $("#"+id+"-charm").data("charm");
    for (var i = 0; i < charms.length; i++){
        if (charms[i] != charm) {
            if (charms[i].element.data("opened") === true) {
                charms[i].close();
            }
        }
    }
    if (charm.element.data("opened") === true) {
        charm.close();
    } else {
        charm.open();
    }
}

function closeCharm(id){
    var charm = $("#"+id+"-charm").data("charm");
    if (charm.element.data("opened") === true) {
        charm.close();
    }
}
