
function startFunction() {
    // Make an AJAX request to start the function
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/start_function', true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Function started successfully
            pollProgress();
        }
    };

    xhr.send();
}

function pollProgress() {
    // Poll the server for progress updates
    var interval = setInterval(function () {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/get_progress', true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var progress = JSON.parse(xhr.responseText);
                document.getElementById('progressBar').value = progress.percent;
                document.getElementById('progressText').innerText = 'Progress: ' + progress.percent + '%';

                // Check if the function is complete
                if (progress.percent == 100) {
                    clearInterval(interval);
                }
            }
        };

        xhr.send();
    }, 1000); // Adjust the interval as needed
}
