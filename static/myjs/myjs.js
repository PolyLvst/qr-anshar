var successDing = "../static/assets/ding.mp3";
let idleTime = 3; //Seconds

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

const checkImage = (url, callback) => {
    const img = new Image();
    img.onload = () => callback(true);
    img.onerror = () => callback(false);
    img.src = url;
};

function loadStudentPicture(id) {
    const pictureBox = $("#picture-box");
    const pngUrl = `../static/assets/student-pictures/${id}.png`;
    const jpgUrl = `../static/assets/student-pictures/${id}.jpg`;
    let tempHtml;

    // Try loading .jpg first
    checkImage(jpgUrl, (exists) => {
        if (exists) {
            tempHtml = `<div class="image-container-murid">
            <img src='../static/assets/student-pictures/${id}.jpg' alt="" id="picture-student" class="profile-icon rounded mx-auto d-block">
            </div>`;
            pictureBox.empty();
            pictureBox.append(tempHtml);
        } else {
            // Fallback to .png if .jpg doesn't exist
            checkImage(pngUrl, (exists) => {
                if (exists) {
                    tempHtml = `<div class="image-container-murid">
                                    <img src='../static/assets/student-pictures/${id}.png' alt="" id="picture-student" class="profile-icon rounded mx-auto d-block">
                                </div>`;
                } else {
                    // Handle case if no image exists
                    tempHtml = `<div class="image-container-murid">
                                        <img src="../static/assets/person-bounding-box.svg" alt="" id="picture-student" class="profile-icon rounded mx-auto d-block">
                                    </div>`;
                }
                pictureBox.empty();
                pictureBox.append(tempHtml);
            });
        }
    });
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
            const alertSection = $("#alert-section");
            const borderScan = $("#border-scan");
            const pictureBox = $("#picture-box");

            pictureArea.empty();
            welcomeSection.empty();
            alertSection.empty();
            borderScan.removeClass("border-info");
            borderScan.removeClass("border-success");
            pictureBox.empty();

            if (response["status"] == "oke") {
                absenSiswa(id);
                let data = response["data"];
                let name = data["name"];
                loadStudentPicture(id);
                let tempHtml = `
                <h5>Selamat datang ${name}<h5>
                </br>
                `;
                welcomeSection.append(tempHtml);
            } else {
                let warningHtml = `
                <div class="row justify-content-center">
                    <div class="alert alert-danger d-flex align-items-center w-50" role="alert">
                        <img class="bi flex-shrink-2 me-2" src="../static/assets/exclamation-triangle-fill.svg" alt="warning icon">
                        <div>Siswa/i tidak ditemukan</div>
                    </div>
                </div>`;
                alertSection.append(warningHtml);
            }
        }
    })
};

function absenSiswa(id) {
    $.ajax({
        "type": "POST",
        "url": "/api/absen",
        "data": {
            "nis": id,
            "tipe": "masuk"
        },
        success: function (response) {
            const pictureArea = $("#menunggu-scan-text");
            const alertSection = $("#alert-section");
            const borderScan = $("#border-scan");

            pictureArea.empty();
            alertSection.empty();
            borderScan.removeClass("border-info");
            borderScan.removeClass("border-success");

            if (response["status"] == "oke") {
                playSound(successDing);
                // window.alert("Sukses")
                let warningHtml = `
                <div class="row justify-content-center">
                    <div class="alert alert-success d-flex align-items-center w-50" role="alert">
                        <img class="bi flex-shrink-2 me-2" src="../static/assets/success.svg" alt="success icon">
                        <div>Terabsen</div>
                    </div>
                </div>`;
                borderScan.addClass("border-success");
                alertSection.append(warningHtml);
            } else {
                // window.alert("Telah terabsen")
                let warningHtml = `
                <div class="row justify-content-center">
                    <div class="alert alert-info d-flex align-items-center w-50" role="alert">
                        <img class="bi flex-shrink-2 me-2" src="../static/assets/info.svg" alt="info icon">
                        <div>Telah terabsen</div>
                    </div>
                </div>`;
                borderScan.addClass("border-info");
                alertSection.append(warningHtml);
            }
        }
    })
};

function replenishWaitingMessage() {
    const borderScan = $("#border-scan");
    const pictureBox = $("#picture-box");
    const pictureArea = $("#menunggu-scan-text");
    const welcomeSection = $("#welcome-section");
    const alertSection = $("#alert-section");

    let tempHtml = `
    <h5>Scan QR</h5>
    <p id="text-menunggu">Menunggu .</p>
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>`;
    welcomeSection.empty();
    pictureArea.empty();
    pictureBox.empty();
    pictureBox.append(`<div class="image-container">
                            <img src="../static/assets/person-bounding-box.svg" alt="" id="picture-student" class="profile-icon">
                        </div>`);
    pictureArea.append(tempHtml);
    borderScan.removeClass("border-info");
    borderScan.removeClass("border-success");
    alertSection.empty();
};

function clearOrResetInput() {
    $(':input')
        .not(':button, :submit, :reset, :hidden')
        .removeAttr('checked')
        .removeAttr('selected')
        .not(':checkbox, :radio, select')
        .val('');
};

function detectTextInput() {
    //     checkBox = $("#autoSubmitCheckbox");
    const inputElement = $("#text-input-scan");
    $("#text-input-scan").keypress(function (event) {
        if (event.which === 13) { // 13 is the key code for Enter
            let inputStr = inputElement.val().trim();
            clearOrResetInput();
            getNameById(inputStr);
        };
    });

    //     // $("#text-input-scan").on("keydown",function(event) {
    //     //     if (event.keyCode === 8) { // 8 is the key code for Backspace
    //     //         alert("Backspace");
    //     //     };
    //     // });

    //     inputElement.on("input", function () {
    //         if (checkBox.is(":checked")){
    //             let inputStr = inputElement.val().trim();
    //             if (inputStr !== "" && inputStr.length >= 4) {
    //                 getNameById(inputStr);
    //             };
    //         };
    //     });
};

function detectIdle() {
    var currSeconds = 0;
    let idleInterval = setInterval(timerIncrement, 1000);
    // $(this).mousemove(resetTimer);
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