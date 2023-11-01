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
        setTimeout(function() {
            clearInterval(intervalId);
            loadingDots.text("Menunggu ...");
        }, 10000);
    }
    animateLoadingDots();
};

function loadStudentPicture(id){
    const pictureBox = $("#picture-box");
    let tempHtml = `<img src="../static/assets/student-pictures/${id}.jpg" alt="" id="picture-student" class="profile-icon">`;
    pictureBox.empty();
    pictureBox.append(tempHtml);
};

function getNameById(id){
    let url = "/api/getid/"+id;
    $.ajax({
        "type":"GET",
        "url":url,
        "data":{},
        success: function(response){
            let data = response["data"];
            let name = data["name"];
            let classStu = data["class"];
            const pictureArea = $("#menunggu-scan-text");
            pictureArea.empty()
            loadStudentPicture(id);
        }
    })
}

function detectTextInput(){
    const inputElement = $("#text-input-scan");
    const statusElement = $("#status");

    inputElement.on("input", function() {
        let inputStr = inputElement.val().trim();
        if (inputStr !== "" && inputStr.length >= 4) {
            statusElement.text("Text has been filled.");
            getNameById(inputStr)
        } else {
            statusElement.text("");
        }
    });
}