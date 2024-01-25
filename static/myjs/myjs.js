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

function loadStudentPicture(id) {
    const pictureBox = $("#picture-box");
    let tempHtml = `<div class="image-container-murid">
                        <img src='../static/assets/student-pictures/${id}.jpg' alt="" id="picture-student" class="profile-icon rounded mx-auto d-block">
                    </div>`;
    pictureBox.empty();
    pictureBox.append(tempHtml);
};

function getClassrooms(targ_id) {
    const classSelects = $(targ_id);

    let tempHtml = `<option selected value="">Pilih - kelas</option>`;
    classSelects.empty();
    classSelects.append(tempHtml);
    let url = "/api/get_classrooms";
    $.ajax({
        "type": "GET",
        "url": url,
        "data": {},
        success: function (response) {
            let classes = response["data"];
            // console.log(classes);
            for (let key in classes) {
                let value_id = classes[key]["id"];
                let value_name = classes[key]["class_name"];
                let tempHtml = `<option value="${value_id}">${value_name}</option>`;
                classSelects.append(tempHtml);
            };
        }
    });
};

function addStudent() {
    let inputNis = $("#input-nis").val();
    let namaStu = $("#input-nama").val();
    let idKelas = $("#input-kelas").val();
    let fileImg = $("#input-foto").prop("files")[0];

    let is_alert = "";
    if (!inputNis) { is_alert += "masukkan nis " }
    if (!namaStu) { is_alert += "masukkan nama " }
    if (idKelas == "") { is_alert += "pilih kelas " }
    if (!fileImg) { is_alert += "pilih foto " }
    if (is_alert) {
        alert(is_alert);
        return;
    }

    const formData = new FormData();
    formData.append("nis", inputNis);
    formData.append("nama", namaStu);
    formData.append("kelas", idKelas);
    formData.append("file", fileImg);
    $.ajax({
        "type": "POST",
        "url": "/api/add_student",
        "data": formData,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["status"] == "success") {
                alert(response["msg"]);
            } else if (response["status"] == "failed") {
                alert(response["msg"]);
            } else {
                window.location.href = "/login";
            }
        }
    });
};

function editStudent() {
    let inputNis = $("#input-nis-edit").val();
    let namaStu = $("#input-nama-edit").val();
    let idKelas = $("#input-kelas-edit").val();
    let fileImg = $("#input-foto-edit").prop("files")[0];

    let is_alert = "";
    if (!inputNis) { is_alert += "masukkan nis " }
    if (!namaStu) { is_alert += "masukkan nama " }
    if (idKelas == "") { is_alert += "pilih kelas " }
    // if (!fileImg) { is_alert += "pilih foto " }
    if (is_alert) {
        alert(is_alert);
        return;
    }

    const formData = new FormData();
    formData.append("nis", inputNis);
    formData.append("nama", namaStu);
    formData.append("kelas", idKelas);
    formData.append("file", fileImg);
    $.ajax({
        "type": "POST",
        "url": "/api/edit_student",
        "data": formData,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["status"] == "success") {
                alert(response["msg"]);
            } else if (response["status"] == "failed") {
                alert(response["msg"]);
            } else {
                window.location.href = "/login";
            }
        }
    });
};

function checkIdExist(target_id, mode = "check") {
    // #input-nis
    let id = $(target_id).val()
    let url = "/api/getid/" + id;
    $.ajax({
        "type": "GET",
        "url": url,
        "data": {},
        success: function (response) {
            const inputNis = $(target_id);
            const modalEdit = $("#modal-edit-inputs");
            inputNis.removeClass("is-valid");
            inputNis.removeClass("is-invalid");
            let tempHtml;
            let tempHtmlClass;
            if (response["data"]){
                let nama = response["data"]["name"];
                let kelas = response["data"]["class"];
                let kelas_id = response["data"]["class_id"];
                tempHtml = `
                <div class="input-group mb-2">
                    <input type="text" class="form-control" placeholder="Nama" id="input-nama-edit" value="${nama}">
                </div>
                <div class="input-group mb-2">
                    <select required class="form-select form-select-sm" aria-label="Small select example" placeholder="Kelas id" id="input-kelas-edit">
                    </select>
                </div>
                <div class="input-group">
                    <input type="file" class="form-control" id="input-foto-edit">
                </div>
                `;
                tempHtmlClass = `<option selected value="${kelas_id}">${kelas}</option>`;
            }
            if (response["status"] == "oke") {
                if (mode == "check") {
                    // Siswa sudah ada di database, id terpakai
                    inputNis.addClass("is-invalid");
                } else {
                    // Mode cari nis, id valid dan ada di database
                    inputNis.addClass("is-valid");
                    modalEdit.empty();
                    modalEdit.append(tempHtml);
                    getClassrooms("#input-kelas-edit");
                    $('#input-kelas-edit').append(tempHtmlClass);
                }
            } else {
                if (mode == "check") {
                    // Siswa sudah ada di database, id dapat dipakai untuk siswa baru
                    inputNis.addClass("is-valid");
                } else {
                    // Mode cari nis, id valid dan ada di database
                    inputNis.addClass("is-invalid");
                    modalEdit.empty();
                    modalEdit.append(tempHtml);
                    getClassrooms("#input-kelas-edit");
                    $('#input-kelas-edit').append(tempHtmlClass);
                }
            };
        }
    })
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
                let classStu = data["class"];
                loadStudentPicture(id);
                let tempHtml = `
                <h5>Selamat datang ${name}<h5>
                <p>Kelas ${classStu}<p>
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

function sign_in() {
    let username = $("#input-username").val();
    let password = $("#input-password").val();

    if (username === "") {
        $("#help-id-login").text("Enter your id.");
        $("#input-username").focus();
        return;
    } else {
        $("#help-id-login").text("");
    }

    if (password === "") {
        $("#help-password-login").text("Enter your password.");
        $("#input-password").focus();
        return;
    } else {
        $("#help-password-login").text("");
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            'username_give': username,
            'password_give': password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                let token = response['token'];
                $.cookie("token", token, { path: "/" });
                alert('Login successfully');
                window.location.replace("/");
            } else {
                alert(response["msg"]);
            };
        },
    });
};

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

function logout() {
    deleteCookie("token");
    alert("Logout success")
    window.location.href = "/";
}