function set_tab(name){
    let active_tabs = document.querySelectorAll(".is-active");
    active_tabs.forEach(tab => {
        if (tab.classList.contains("tab")){
            tab.classList.remove("is-active");
        }
    })
    let tab = document.querySelector("#tab-"+name);
    tab.classList.add("is-active");
}