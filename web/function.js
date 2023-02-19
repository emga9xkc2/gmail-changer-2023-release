$(document).ready(function () {
    loadHome().then(loadImport).then(loadChucNang);
    $.getScript("/codinglab.js", function () {
        // Code để gọi hàm hoặc xử lý dữ liệu tại đây
    });
    loadSidebar();
});

function loadSidebarHtml() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "html/sidebar.html",
            success: function (result) {
                $("#load-sidebar").html(result);
                resolve();
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}
function loadHome() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "html/home.html",
            success: function (result) {
                $("#load-home").html(result);
                resolve();
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}
function loadImport() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "html/import.html",
            success: function (result) {
                $("#load-import").html(result);
                resolve();
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}
function loadChucNang() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "html/chucnang.html",
            success: function (result) {
                $("#load-chucnang").html(result);
                resolve();
            },
            error: function (error) {
                reject(error);
            },
        });
    });
}

function openMenu(evt, cityName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("tabs");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(
            " menuselected",
            ""
        );
    }
    document.getElementById(cityName).style.display = "block";
    // console.log(evt.currentTarget)
    evt.currentTarget.className += " menuselected";
    var linkName = evt.currentTarget.querySelector(".link_name").textContent;
    document.getElementById("title").textContent = linkName;
}

function loadSidebar() {
    let arrow = document.querySelectorAll(".arrow");
    for (var i = 0; i < arrow.length; i++) {
        arrow[i].addEventListener("click", (e) => {
            let arrowParent = e.target.parentElement.parentElement; //selecting main parent of arrow
            arrowParent.classList.toggle("showMenu");
        });
    }
    let sidebar = document.querySelector(".sidebar");
    let sidebarBtn = document.querySelector(".bx-menu");
    // console.log(sidebarBtn);
    sidebarBtn.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });

    // let logout = document.querySelector(".logout");
    // logout.addEventListener("click", () => {
    // 	eel.openFileDialog()(function (callback) {
    // 		console.log(callback)
    // 	}
    // 	)
    // });
}
function msgBox(text) {
    alert(text);
}

eel.getTitle()(function (callback) {
    document.title = callback;
});
