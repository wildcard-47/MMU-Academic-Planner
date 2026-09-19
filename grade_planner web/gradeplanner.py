from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


 # ==========================================================
# HOME PAGE
# ==========================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Grade Planner</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #fbdcee;
            }


            .home {
                min-height: 100vh;
                text-align: center;
                padding-top: 40px;

                background: linear-gradient(
                    135deg,
                    #fff5fa,
                    #fbd6e9
                );
            }


            /* TITLE */

            h1 {
                color: #be165f;
                font-size: 40px;
                margin-top: 0;
                margin-bottom: 10px;
            }


            /* CLOUD CONTAINER */

            .cloud-container {
                display: grid;

                grid-template-columns: 1fr 1fr;

                gap: 20px;

                max-width: 750px;

                margin: auto;
            }


            /* CLOUD */

            .cloud {
                position: relative;

                width: 320px;
                height: 150px;

                margin: auto;

                cursor: pointer;

                transition: transform 0.2s;
            }


            .cloud:hover {
                transform: scale(1.08);
            }


            /* CLOUD BOTTOM */

            .cloud-bottom {
                position: absolute;

                width: 270px;
                height: 80px;

                left: 25px;
                top: 55px;

                background: white;

                border-radius: 60px;

                box-shadow:
                    0 8px 18px rgba(190, 22, 95, 0.2);
            }


            /* LEFT CLOUD */

            .cloud-left {
                position: absolute;

                width: 100px;
                height: 100px;

                left: 55px;
                top: 10px;

                background: white;

                border-radius: 50%;
            }


            /* RIGHT CLOUD */

            .cloud-right {
                position: absolute;

                width: 125px;
                height: 125px;

                right: 55px;
                top: 0;

                background: white;

                border-radius: 50%;
            }


            /* CLOUD TEXT */

            .cloud-text {
                position: absolute;

                width: 270px;

                left: 25px;
                top: 78px;

                z-index: 10;

                color: #be165f;

                font-size: 17px;
                font-weight: bold;

                text-align: center;
            }


            /* MOBILE */

            @media (max-width: 700px) {

                .cloud-container {
                    grid-template-columns: 1fr;
                }

            }

        </style>

    </head>


    <body>

        <div class="home">

            <h1>GRADE PLANNER</h1>


            <div class="cloud-container">


                <!-- CLOUD 1 -->

                <div class="cloud"
                     onclick="window.location.href='/overall'">

                    <div class="cloud-left"></div>
                    <div class="cloud-right"></div>
                    <div class="cloud-bottom"></div>

                    <div class="cloud-text">
                        CALCULATE OVERALL<br>
                        PERFORMANCE
                    </div>

                </div>


                <!-- CLOUD 2 -->

                <div class="cloud"
                     onclick="window.location.href='/target'">

                    <div class="cloud-left"></div>
                    <div class="cloud-right"></div>
                    <div class="cloud-bottom"></div>

                    <div class="cloud-text">
                        CONVERT TO PERCENTAGE &<br>
                        SELECT A TARGET GRADE
                    </div>

                </div>


                <!-- CLOUD 3 -->

                <div class="cloud"
                     onclick="window.location.href='/minimum-score'">

                    <div class="cloud-left"></div>
                    <div class="cloud-right"></div>
                    <div class="cloud-bottom"></div>

                    <div class="cloud-text">
                        MINIMUM SCORE<br>
                        REQUIRED
                    </div>

                </div>


                <!-- CLOUD 4 -->

                <div class="cloud"
                     onclick="window.location.href='/what-if'">

                    <div class="cloud-left"></div>
                    <div class="cloud-right"></div>
                    <div class="cloud-bottom"></div>

                    <div class="cloud-text">
                        WHAT-IF<br>
                        CALCULATOR
                    </div>

                </div>


            </div>

        </div>

    </body>

    </html>
    """


# ==========================================================
# CURRENT OVERALL PERFORMANCE
# ==========================================================

@app.get("/overall", response_class=HTMLResponse)
def overall():

    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Current Overall Performance</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #fbdcee;
            }

            .container {
                max-width: 900px;
                margin: auto;
                padding: 30px;
            }

            h1 {
                text-align: center;
                color: #BE165F;
            }

            .assessment {
                background: white;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 12px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }

            .row {
                display: grid;
                grid-template-columns: 2fr 1fr 1fr auto;
                gap: 10px;
                align-items: center;
            }

            input {
                width: 100%;
                padding: 10px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 7px;
                font-size: 15px;
            }

            button {
                margin-top: 10px;
                padding: 11px 18px;
                border: none;
                border-radius: 8px;
                background: #BE165F;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #9e124f;
            }

            .remove {
                margin-top: 0;
                background: #777;
            }

            .remove:hover {
                background: #555;
            }

            .add-button {
                background: #e8a6c5;
                color: #7c1645;
            }

            .result-box {
                background: #FBDCEE;
                padding: 20px;
                margin-top: 25px;
                border-radius: 12px;
            }

            .error {
                color: #c0392b;
                font-weight: bold;
            }

            .back {
                background: #777;
            }

            @media (max-width: 700px) {

                .row {
                    grid-template-columns: 1fr;
                }

            }

        </style>
    </head>


    <body>

        <div class="container">

            <h1>CURRENT OVERALL PERFORMANCE</h1>

            <div id="assessments">

                <div class="assessment">

                    <div class="row">

                        <input
                            type="text"
                            class="assessment-name"
                            placeholder="Assessment name"
                        >

                        <input
                            type="number"
                            class="score"
                            min="0"
                            max="100"
                            step="0.01"
                            placeholder="Mark %"
                        >

                        <input
                            type="number"
                            class="weight"
                            min="1"
                            max="100"
                            step="0.01"
                            placeholder="Weight %"
                        >

                        <button
                            class="remove"
                            onclick="removeAssessment(this)">
                            REMOVE
                        </button>

                    </div>

                </div>

            </div>


            <button
                class="add-button"
                onclick="addAssessment()">

                + ADD ASSESSMENT

            </button>


            <br>


            <button onclick="calculateOverall()">
                CALCULATE
            </button>


            <p id="error" class="error"></p>


            <div id="results"></div>


            <button
                class="back"
                onclick="window.location.href='/'">

                BACK TO HOME

            </button>

        </div>


        <script>

            // ==================================================
            // ADD ASSESSMENT
            // ==================================================

            function addAssessment() {

                const assessments =
                    document.getElementById("assessments");

                const newAssessment =
                    document.createElement("div");

                newAssessment.className =
                    "assessment";

                newAssessment.innerHTML = `

                    <div class="row">

                        <input
                            type="text"
                            class="assessment-name"
                            placeholder="Assessment name"
                        >

                        <input
                            type="number"
                            class="score"
                            min="0"
                            max="100"
                            step="0.01"
                            placeholder="Mark %"
                        >

                        <input
                            type="number"
                            class="weight"
                            min="1"
                            max="100"
                            step="0.01"
                            placeholder="Weight %"
                        >

                        <button
                            class="remove"
                            onclick="removeAssessment(this)">
                            REMOVE
                        </button>

                    </div>

                `;

                assessments.appendChild(newAssessment);
            }


            // ==================================================
            // REMOVE ASSESSMENT
            // ==================================================

            function removeAssessment(button) {

                button
                    .closest(".assessment")
                    .remove();

            }


            // ==================================================
            // CALCULATE OVERALL
            // ==================================================

            function calculateOverall() {

                const assessments =
                    document.querySelectorAll(".assessment");

                const error =
                    document.getElementById("error");

                const results =
                    document.getElementById("results");

                error.innerHTML = "";
                results.innerHTML = "";

                let totalWeight = 0;
                let currentEarned = 0;


                // ==================================================
                // CHECK EACH ASSESSMENT
                // ==================================================

                for (let i = 0; i < assessments.length; i++) {

                    const assessment =
                        assessments[i];

                    const name =
                        assessment
                        .querySelector(".assessment-name")
                        .value
                        .trim();

                    const score =
                        parseFloat(
                            assessment
                            .querySelector(".score")
                            .value
                        );

                    const weight =
                        parseFloat(
                            assessment
                            .querySelector(".weight")
                            .value
                        );


                    if (name === "") {

                        error.innerHTML =
                            "Please enter a name for every assessment.";

                        return;
                    }


                    if (
                        isNaN(score) ||
                        score < 0 ||
                        score > 100
                    ) {

                        error.innerHTML =
                            "Mark must be between 0 and 100.";

                        return;
                    }


                    if (
                        isNaN(weight) ||
                        weight < 1 ||
                        weight > 100
                    ) {

                        error.innerHTML =
                            "Weight must be between 1 and 100.";

                        return;
                    }


                    // Mark can be higher than weight.
                    // This is completely valid.

                    const weightedMark =
                        score * weight / 100;


                    currentEarned += weightedMark;
                    totalWeight += weight;

                }


                // ==================================================
                // TOTAL WEIGHT MAXIMUM = 100
                // ==================================================

                if (totalWeight > 100) {

                    error.innerHTML =
                        "Total assessment weight cannot be more than 100%.";

                    return;
                }


                // ==================================================
                // REMAINING WEIGHT
                // ==================================================

                const remainingWeight =
                    100 - totalWeight;


                // ==================================================
                // CURRENT PERFORMANCE
                // ==================================================

                let currentPerformance = 0;

                if (totalWeight > 0) {

                    currentPerformance =
                        currentEarned /
                        totalWeight *
                        100;

                }


                // ==================================================
                // HIGHEST POSSIBLE FINAL
                // ==================================================

                const highestFinalMark =
                    Math.min(
                        100,
                        currentEarned + remainingWeight
                    );


                // ==================================================
                // DISPLAY RESULTS
                // ==================================================

                results.innerHTML = `

                    <div class="result-box">

                        <h2>RESULTS</h2>

                        <p>
                            <b>Current Earned:</b>
                            ${currentEarned.toFixed(2)}%
                        </p>

                        <p>
                            <b>Completed Weight:</b>
                            ${totalWeight.toFixed(2)}%
                        </p>

                        <p>
                            <b>Remaining Weight:</b>
                            ${remainingWeight.toFixed(2)}%
                        </p>

                        <p>
                            <b>Current Performance:</b>
                            ${currentPerformance.toFixed(2)}%
                        </p>

                        <p>
                            <b>Highest Possible Final Mark:</b>
                            ${highestFinalMark.toFixed(2)}%
                        </p>

                    </div>

                `;

            }

        </script>

    </body>

    </html>
    """


# ==========================================================
# 2. CONVERT & TARGET GRADE
# ==========================================================

@app.get("/target", response_class=HTMLResponse)
def target():
    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Convert to percentage & select a target grade</title>

        <style>

            body {
                margin: 0;
                font-family: Arial;
                background: #fff0f7;
            }

            .page {
                min-height: 100vh;
                padding: 40px;
            }

            h1 {
                text-align: center;
                color: #be165f;
            }

            .box {
                max-width: 600px;
                margin: 30px auto;
                padding: 30px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 5px 20px #e5b6ca;
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 7px;
                font-weight: bold;
            }

            input,
            select {
                width: 100%;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 15px;
            }

            button {
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                background: #be165f;
                color: white;
                cursor: pointer;
            }

            .result {
                margin-top: 20px;
                padding: 20px;
                background: #fbdcee;
                border-radius: 15px;
            }

            .back {
                background: #777;
                margin-top: 15px;
            }

        </style>

    </head>

    <body>

        <div class="page">

            <h1>CONVERT TO PERCENTAGE & SELECT A TARGET GRADE</h1>

            <div class="box">

                <label>
                    Percentage (%)
                </label>

                <input
                    id="percentage"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Enter percentage">


                <button onclick="convertGrade()">

                    CONVERT GRADE

                </button>


                <div id="convertResult"></div>


                <hr>


                <label>
                    Select Target Grade
                </label>

                <select id="targetGrade">

                    <option value="90">A+</option>
                    <option value="80">A</option>
                    <option value="75">A-</option>
                    <option value="70">B+</option>
                    <option value="65">B</option>
                    <option value="60">B-</option>
                    <option value="55">C+</option>
                    <option value="50">C</option>
                    <option value="45">C-</option>
                    <option value="40">D</option>

                </select>


                <button onclick="showTarget()">

                    SHOW TARGET MARK

                </button>


                <div id="targetResult"></div>


                <button
                    class="back"
                    onclick="window.location.href='/'">

                    BACK TO HOME

                </button>

            </div>

        </div>


        <script>

            function convertGrade() {

                let input =
                    document.getElementById("percentage");

                let mark =
                    Number(input.value);


                if (
                    input.value === "" ||
                    mark < 0 ||
                    mark > 100
                ) {

                    document.getElementById(
                        "convertResult"
                    ).innerHTML = `

                        <div class="result">

                            Percentage must be between
                            0 and 100.

                        </div>

                    `;

                    return;
                }


                document.getElementById(
                    "convertResult"
                ).innerHTML = `

                    <div class="result">

                        <b>Letter Grade:</b>
                        ${getGrade(mark)}

                    </div>

                `;
            }


            function showTarget() {

                let select =
                    document.getElementById("targetGrade");

                let grade =
                    select.options[
                        select.selectedIndex
                    ].text;

                let mark =
                    select.value;


                document.getElementById(
                    "targetResult"
                ).innerHTML = `

                    <div class="result">

                        <b>${grade}</b>
                        requires ${mark}%

                    </div>

                `;
            }


            function getGrade(mark) {

                if (mark >= 90) return "A+";
                if (mark >= 80) return "A";
                if (mark >= 75) return "A-";
                if (mark >= 70) return "B+";
                if (mark >= 65) return "B";
                if (mark >= 60) return "B-";
                if (mark >= 55) return "C+";
                if (mark >= 50) return "C";
                if (mark >= 45) return "C-";
                if (mark >= 40) return "D";

                return "F";
            }

        </script>

    </body>

    </html>
    """

# =========================
# MINIMUM SCORE REQUIRED
# =========================

@app.get("/minimum-score", response_class=HTMLResponse)
def minimum_score():

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Minimum Score Required</title>

        <style>

            body {
                font-family: Arial;
                background-color: #fff0f7;
                margin: 0;
                padding: 30px;
                text-align: center;
            }

            h1 {
                color: #BE165F;
                margin-bottom: 30px;
            }

            .container {
                background-color: white;
                width: 700px;
                max-width: 90%;
                margin: auto;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }

            input {
                width: 80%;
                padding: 12px;
                border: 2px solid #F3B6D2;
                border-radius: 10px;
                font-size: 16px;
            }

            button {
                margin-top: 25px;
                padding: 12px 25px;
                border: none;
                border-radius: 10px;
                background-color: #BE165F;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }

            button:hover {
                background-color: #9e124f;
            }

            #result {
                margin-top: 25px;
                text-align: left;
            }

            .summary {
                background-color: #FBDCEE;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 20px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }

            th {
                background-color: #FBDCEE;
                color: #BE165F;
            }

            .error {
                color: red;
                font-weight: bold;
                margin-top: 15px;
            }

            .back-home {
                display: inline-block;
                margin-top: 30px;
                padding: 12px 25px;
                background-color: #808080;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }

            .back-home:hover {
                background-color: #9e124f;
            }

        </style>

    </head>


    <body>

        <div class="container">

            <h1>MINIMUM SCORE REQUIRED</h1>


            <label>Current Performance (%)</label>

            <input
                type="number"
                id="currentPerformance"
                min="0"
                step="0.01"
                placeholder="Enter"
            >


            <label>Completed Weight (%)</label>

            <input
                type="number"
                id="completedWeight"
                min="0"
                max="100"
                step="0.01"
                placeholder="Enter"
            >


            <br>


            <button onclick="calculateMinimumScore()">
                CALCULATE
            </button>


            <div id="error" class="error"></div>

            <div id="result"></div>


            <!-- BACK HOME AT THE BOTTOM -->

            <a href="/" class="back-home">
                 BACK TO HOME
            </a>

        </div>


        <script> 
            function calculateMinimumScore() {

                let currentPerformance =
                    parseFloat(
                        document.getElementById(
                            "currentPerformance"
                        ).value
                    );


                let completedWeight =
                    parseFloat(
                        document.getElementById(
                            "completedWeight"
                        ).value
                    );


                let error =
                    document.getElementById("error");

                let result =
                    document.getElementById("result");


                error.innerHTML = "";
                result.innerHTML = "";


                // Check Current Performance

                if (
                    isNaN(currentPerformance) ||
                    currentPerformance < 0
                ) {

                    error.innerHTML =
                        "Current Performance cannot be negative.";

                    return;
                }


                // Check Completed Weight

                if (
                    isNaN(completedWeight) ||
                    completedWeight < 0 ||
                    completedWeight > 100
                ) {

                    error.innerHTML =
                        "Completed Weight must be between 0% and 100%.";

                    return;
                }


                // Calculate Current Earned

                let currentEarned =
                    (currentPerformance * completedWeight) / 100;


                // Calculate Remaining Weight

                let remainingWeight =
                    100 - completedWeight;


                // Minimum Score You Can Get

                let minimumScore =
                    currentEarned;


                result.innerHTML = `

                    <div class="summary">

                        <p>
                            <strong>Current Earned:</strong>
                            ${currentEarned.toFixed(2)}%
                        </p>

                        <p>
                            <strong>Completed Weight:</strong>
                            ${completedWeight.toFixed(2)}%
                        </p>

                        <p>
                            <strong>Remaining Weight:</strong>
                            ${remainingWeight.toFixed(2)}%
                        </p>

                        <p>
                            <strong>Minimum Score You Can Get:</strong>
                            ${minimumScore.toFixed(2)}%
                        </p>

                    </div>


                    <h2>Grade Requirements</h2>


                    <table>

                        <tr>
                            <th>Grade</th>
                            <th>Final Overall Range</th>
                            <th>Minimum Score Needed</th>
                        </tr>


                        <tr>
                            <td>A+</td>
                            <td>90–100</td>
                            <td>
                                ${calculateRequiredScore(
                                    90,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>A</td>
                            <td>80–89</td>
                            <td>
                                ${calculateRequiredScore(
                                    80,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>A-</td>
                            <td>75–79</td>
                            <td>
                                ${calculateRequiredScore(
                                    75,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>B+</td>
                            <td>70–74</td>
                            <td>
                                ${calculateRequiredScore(
                                    70,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>B</td>
                            <td>65–69</td>
                            <td>
                                ${calculateRequiredScore(
                                    65,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>B-</td>
                            <td>60–64</td>
                            <td>
                                ${calculateRequiredScore(
                                    60,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>C+</td>
                            <td>55–59</td>
                            <td>
                                ${calculateRequiredScore(
                                    55,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>C</td>
                            <td>50–54</td>
                            <td>
                                ${calculateRequiredScore(
                                    50,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>C-</td>
                            <td>47–49</td>
                            <td>
                                ${calculateRequiredScore(
                                    47,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>D+</td>
                            <td>44–46</td>
                            <td>
                                ${calculateRequiredScore(
                                    44,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>D</td>
                            <td>40–43</td>
                            <td>
                                ${calculateRequiredScore(
                                    40,
                                    currentEarned,
                                    remainingWeight
                                )}
                            </td>
                        </tr>


                        <tr>
                            <td>F</td>
                            <td>0–39</td>
                            <td>
                                Already Achieved
                            </td>
                        </tr>

                    </table>

                `;
            }


            function calculateRequiredScore(
                minimumMark,
                currentEarned,
                remainingWeight
            ) {

                if (remainingWeight === 0) {

                    if (currentEarned >= minimumMark) {
                        return "Already Achieved";
                    }

                    return "Cannot Achieve";
                }


                let requiredScore =
                    (
                        (minimumMark - currentEarned)
                        / remainingWeight
                    ) * 100;


                if (requiredScore <= 0) {
                    return "Already Achieved";
                }


                if (requiredScore > 100) {
                    return "Cannot Achieve";
                }


                return requiredScore.toFixed(2) + "%";
            }

        </script>

    </body>

    </html>
    """

# ==========================================================
# 4. WHAT-IF CALCULATOR
# ==========================================================

@app.get("/what-if", response_class=HTMLResponse)
def what_if():
    return """
    <!DOCTYPE html>
    <html>

    <head>

        <title>What-If Calculator</title>

        <style>

            body {
                margin: 0;
                font-family: Arial;
                background: #fff0f7;
            }

            .page {
                min-height: 100vh;
                padding: 40px;
            }

            h1 {
                text-align: center;
                color: #be165f;
            }

            .box {
                width: 500px;
                max-width: 90%;
                margin: 30px auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 5px 20px #e5b6ca;
            }

            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 6px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #ddd;
            }

            button {
                width: 100%;
                margin-top: 20px;
                padding: 13px;
                border: none;
                border-radius: 10px;
                background: #be165f;
                color: white;
                cursor: pointer;
            }

            .result {
                margin-top: 20px;
                padding: 20px;
                background: #fbdcee;
                border-radius: 15px;
                text-align: center;
            }

            .back {
                background: #777;
            }

        </style>

    </head>


    <body>

        <div class="page">

            <h1>WHAT-IF CALCULATOR</h1>


            <div class="box">


                <label>
                    Current Earned (%)
                </label>

                <input
                    id="earned"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Enter current earned percentage">


                <label>
                    Remaining Weight (%)
                </label>

                <input
                    id="remaining"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Enter remaining weight">


                <label>
                    Hypothetical Score (%)
                </label>

                <input
                    id="score"
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Enter hypothetical score">


                <button onclick="calculateWhatIf()">

                    CALCULATE

                </button>


                <div id="result"></div>


                <button
                    class="back"
                    onclick="window.location.href='/'">

                    BACK TO HOME

                </button>

            </div>

        </div>


        <script>

            function calculateWhatIf() {

                let earnedInput =
                    document.getElementById("earned");

                let remainingInput =
                    document.getElementById("remaining");

                let scoreInput =
                    document.getElementById("score");


                let earned =
                    Number(earnedInput.value);

                let remaining =
                    Number(remainingInput.value);

                let score =
                    Number(scoreInput.value);


                if (
                    earnedInput.value === "" ||
                    earned < 0 ||
                    earned > 100
                ) {

                    showError(
                        "Current Earned must be between 0 and 100."
                    );

                    return;
                }


                if (
                    remainingInput.value === "" ||
                    remaining < 0 ||
                    remaining > 100
                ) {

                    showError(
                        "Remaining Weight must be between 0 and 100."
                    );

                    return;
                }


                if (
                    scoreInput.value === "" ||
                    score < 0 ||
                    score > 100
                ) {

                    showError(
                        "Hypothetical Score must be between 0 and 100."
                    );

                    return;
                }


                let projected =
                    earned +
                    (score * remaining / 100);


                document.getElementById(
                    "result"
                ).innerHTML = `

                    <div class="result">

                        <b>Projected Overall Score:</b>

                        <h2>
                            ${projected.toFixed(2)}%
                        </h2>

                    </div>

                `;

            }


            function showError(message) {

                document.getElementById(
                    "result"
                ).innerHTML = `

                    <div class="result">
                        ${message}
                    </div>

                `;

            }

        </script>

    </body>

    </html>
    """