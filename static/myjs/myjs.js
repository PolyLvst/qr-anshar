var successDing = "../static/assets/ding.mp3";
let idleTime = 3 //Seconds

function loadingAnim() {
    const loadingDots = $("#text-menunggu");

    function animateLoadingDots() {
        let dots = 1;
        function updateDots() {
            loadingDots.text("Menunggu " + ".".repeat(dots));
            dots = (dots % 3) + 1;
        }
        updateDots();
        const intervalId = setInterval(updateDots, 500);// Change the dots every 500ms
        // Stop the animation after a certain duration (e.g., 10000ms or 10 seconds)
        setTimeout(function () {
            clearInterval(intervalId);
            loadingDots.text("Menunggu ...");
        }, 10000);
    }
    animateLoadingDots();
};

function loadStudentPicture(id) {
    const pictureBox = $("#picture-box");
    let tempHtml = `<img src="../static/assets/student-pictures/${id}.jpg" alt="" id="picture-student" class="profile-icon">`;
    pictureBox.empty();
    pictureBox.append(tempHtml);
};

function getNameById(id) {
    let url = "/api/getid/" + id;
    $.ajax({
        "type": "GET",
        "url": url,
        "data": {},
        success: function (response) {
            const pictureArea = $("#menunggu-scan-text");
            const welcomeSection = $("#welcome-section");
            if (response["status"] == "oke") {
                absenSiswa(id);
                let data = response["data"];
                let name = data["name"];
                let classStu = data["class"];

                pictureArea.empty()
                welcomeSection.empty()
                loadStudentPicture(id);

                let tempHtml = `
                <h5>Selamat datang ${name}<h5>
                <p>Kelas ${classStu}<p>
                `;
                welcomeSection.append(tempHtml);
            } else {
                pictureArea.empty()
                welcomeSection.empty()
                let warningHtml = `
                <div class="row justify-content-center">
                    <div class="alert alert-danger d-flex align-items-center w-50" role="alert">
                        <img class="bi flex-shrink-2 me-2" src="../static/assets/exclamation-triangle-fill.svg" alt="warning icon">
                        <div>Siswa/i tidak ditemukan</div>
                    </div>
                </div>`;
                welcomeSection.append(warningHtml);
            }
        }
    })
};

function absenSiswa(id) {
    $.ajax({
        "type":"POST",
        "url":"/api/absen",
        "data":{
            "nis":id,
            "tipe":"masuk"
        },
        success:function(response){
            if (response["status"] == "oke"){
                playSound(successDing);
                window.alert("Sukses")
            } else {
                window.alert("Telah terabsen")
            }
        }
    })
};

function replenishWaitingMessage() {
    const pictureBox = $("#picture-box");
    const pictureArea = $("#menunggu-scan-text");
    const welcomeSection = $("#welcome-section");
    let tempHtml = `
    <h5>Scan QR</h5>
    <p id="text-menunggu">Menunggu .</p>
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>`;
    welcomeSection.empty();
    pictureArea.empty();
    pictureBox.empty();
    pictureBox.append(`<img src="../static/assets/person-bounding-box.svg" alt="" id="picture-student" class="profile-icon">`);
    pictureArea.append(tempHtml);
};

function detectTextInput() {
    const inputElement = $("#text-input-scan");
    const statusElement = $("#status");

    inputElement.on("input", function () {
        let inputStr = inputElement.val().trim();
        if (inputStr !== "" && inputStr.length >= 4) {
            statusElement.text("Text has been filled.");
            getNameById(inputStr)
        } else {
            statusElement.text("");
        }
    });
};

function detectIdle() {
    var currSeconds = 0;
    let idleInterval = setInterval(timerIncrement, 1000);
    $(this).mousemove(resetTimer);
    $(this).keypress(resetTimer);
    function resetTimer() {
        currSeconds = 0;
    }
    function timerIncrement() {
        if (currSeconds == idleTime) {
            // console.log('No interaction detected after .. seconds');
            replenishWaitingMessage();
            loadingAnim();
        }
        currSeconds = currSeconds + 1;
    }
};

function playSound(src) {
    // Create an Audio object
    var audio = new Audio(src);
    audio.play();
};