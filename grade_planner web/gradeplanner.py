from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import json

app = FastAPI()

DATABASE = "gradeplanner.db"


# DATABASE


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    
    #1- CALCULATE OVERALL PERFORMANCE


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score REAL,
            weight REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS overall_performance (
            id INTEGER PRIMARY KEY,
            current_earned REAL,
            completed_weight REAL,
            remaining_weight REAL,
            current_performance REAL,
            highest_possible REAL
        )
    """)

    
    #2- TARGET GRADE
    

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS target_grade (
            id INTEGER PRIMARY KEY,
            percentage REAL,
            converted_grade TEXT,
            target_grade TEXT
        )
    """)

    
    #3 - MINIMUM SCORE REQUIRED
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS minimum_score (
            id INTEGER PRIMARY KEY,
            current_performance REAL,
            completed_weight REAL,
            current_earned REAL,
            remaining_weight REAL,
            minimum_score REAL,
            minimum_scores TEXT
        )
    """)

    
    #4- WHAT-IF CALCULATOR
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS what_if (
            id INTEGER PRIMARY KEY,
            earned REAL,
            remaining REAL,
            hypothetical_score REAL,
            projected_score REAL
        )
    """)

    conn.commit()
    conn.close()


create_database()



# SAVE ALL DATA

@app.post("/save-all")
async def save_all(data: dict):

    conn = get_connection()
    cursor = conn.cursor()
 
   
    # 1
    

    if "assessments" in data:

        cursor.execute("DELETE FROM assessments")

        for assessment in data["assessments"]:

            cursor.execute("""
                INSERT INTO assessments
                (name, score, weight)
                VALUES (?, ?, ?)
            """, (
                assessment.get("name", ""),
                assessment.get("score"),
                assessment.get("weight")
            ))

    if any(key in data for key in [
        "current_earned",
        "completed_weight",
        "remaining_weight",
        "current_performance",
        "highest_possible"
    ]):

        cursor.execute("""
            INSERT OR IGNORE INTO overall_performance
            (id)
            VALUES (1)
        """)

        if "current_earned" in data:

            cursor.execute("""
                UPDATE overall_performance
                SET current_earned = ?
                WHERE id = 1
            """, (data["current_earned"],))

        if "completed_weight" in data:

            cursor.execute("""
                UPDATE overall_performance
                SET completed_weight = ?
                WHERE id = 1
            """, (data["completed_weight"],))

        if "remaining_weight" in data:

            cursor.execute("""
                UPDATE overall_performance
                SET remaining_weight = ?
                WHERE id = 1
            """, (data["remaining_weight"],))

        if "current_performance" in data:

            cursor.execute("""
                UPDATE overall_performance
                SET current_performance = ?
                WHERE id = 1
            """, (data["current_performance"],))

        if "highest_possible" in data:

            cursor.execute("""
                UPDATE overall_performance
                SET highest_possible = ?
                WHERE id = 1
            """, (data["highest_possible"],))


    
    #  2
    
    if any(key in data for key in [
        "percentage",
        "converted_grade",
        "target_grade"
    ]):

        cursor.execute("""
            INSERT OR IGNORE INTO target_grade
            (id)
            VALUES (1)
        """)

        if "percentage" in data:

            cursor.execute("""
                UPDATE target_grade
                SET percentage = ?
                WHERE id = 1
            """, (data["percentage"],))

        if "converted_grade" in data:

            cursor.execute("""
                UPDATE target_grade
                SET converted_grade = ?
                WHERE id = 1
            """, (data["converted_grade"],))

        if "target_grade" in data:

            cursor.execute("""
                UPDATE target_grade
                SET target_grade = ?
                WHERE id = 1
            """, (data["target_grade"],))


    
    # 3
    
    if any(key in data for key in [
        "minimum_current_performance",
        "minimum_completed_weight",
        "minimum_current_earned",
        "minimum_remaining_weight",
        "minimum_score",
        "minimum_scores"
    ]):

        cursor.execute("""
            INSERT OR IGNORE INTO minimum_score
            (id)
            VALUES (1)
        """)

        if "minimum_current_performance" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET current_performance = ?
                WHERE id = 1
            """, (
                data["minimum_current_performance"],
            ))

        if "minimum_completed_weight" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET completed_weight = ?
                WHERE id = 1
            """, (
                data["minimum_completed_weight"],
            ))

        if "minimum_current_earned" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET current_earned = ?
                WHERE id = 1
            """, (
                data["minimum_current_earned"],
            ))

        if "minimum_remaining_weight" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET remaining_weight = ?
                WHERE id = 1
            """, (
                data["minimum_remaining_weight"],
            ))

        if "minimum_score" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET minimum_score = ?
                WHERE id = 1
            """, (
                data["minimum_score"],
            ))

        if "minimum_scores" in data:

            cursor.execute("""
                UPDATE minimum_score
                SET minimum_scores = ?
                WHERE id = 1
            """, (
                json.dumps(data["minimum_scores"]),
            ))


    
    # 4
    
    if any(key in data for key in [
        "earned",
        "remaining",
        "hypothetical_score",
        "projected_score"
    ]):

        cursor.execute("""
            INSERT OR IGNORE INTO what_if
            (id)
            VALUES (1)
        """)

        if "earned" in data:

            cursor.execute("""
                UPDATE what_if
                SET earned = ?
                WHERE id = 1
            """, (data["earned"],))

        if "remaining" in data:

            cursor.execute("""
                UPDATE what_if
                SET remaining = ?
                WHERE id = 1
            """, (data["remaining"],))

        if "hypothetical_score" in data:

            cursor.execute("""
                UPDATE what_if
                SET hypothetical_score = ?
                WHERE id = 1
            """, (data["hypothetical_score"],))

        if "projected_score" in data:

            cursor.execute("""
                UPDATE what_if
                SET projected_score = ?
                WHERE id = 1
            """, (data["projected_score"],))


    # IMPORTANT
    conn.commit()
    conn.close()

    return {
        "message": "Data saved successfully"
    }



#LOAD ALL DATA

@app.get("/load-all")
async def load_all():

    conn = get_connection()
    cursor = conn.cursor()

    
    # FEATURE 1 - LOAD
    
    cursor.execute("""
        SELECT name, score, weight
        FROM assessments
    """)

    rows = cursor.fetchall()

    assessments = []

    for row in rows:

        assessments.append({
            "name": row[0],
            "score": row[1],
            "weight": row[2]
        })

    cursor.execute("""
        SELECT
            current_earned,
            completed_weight,
            remaining_weight,
            current_performance,
            highest_possible
        FROM overall_performance
        WHERE id = 1
    """)

    row = cursor.fetchone()

    overall_data = None

    if row:

        overall_data = {
            "current_earned": row[0],
            "completed_weight": row[1],
            "remaining_weight": row[2] ,
            "current_performance": row[3],
            "highest_possible": row[4]
        }


   
    # 2 - LOAD
    
    cursor.execute("""
        SELECT
            percentage,
            converted_grade,
            target_grade
        FROM target_grade
        WHERE id = 1
    """)

    row = cursor.fetchone()

    target_data = None

    if row:

        target_data = {
            "percentage": row[0],
            "converted_grade": row[1],
            "target_grade": row[2]
        }


    
    #3 - LOAD


    cursor.execute("""
        SELECT
            current_performance,
            completed_weight,
            current_earned,
            remaining_weight,
            minimum_score,
            minimum_scores
        FROM minimum_score
        WHERE id = 1
    """)

    row = cursor.fetchone()

    minimum_data = None

    if row:

        minimum_data = {
            "current_performance": row[0],
            "completed_weight": row[1],
            "current_earned": row[2],
            "remaining_weight": row[3],
            "minimum_score": row[4],
            "minimum_scores":
                json.loads(row[5])
                if row[5]
                else {}
        }


    
    #4 - LOAD
    
    cursor.execute("""
        SELECT
            earned,
            remaining,
            hypothetical_score,
            projected_score
        FROM what_if
        WHERE id = 1
    """)

    row = cursor.fetchone()

    what_if_data = None

    if row:

        what_if_data = {
            "earned": row[0],
            "remaining": row[1],
            "hypothetical_score": row[2],
            "projected_score": row[3]
        }


    conn.close()

    return {

        "assessments": assessments,

        "overall_performance":
            overall_data,

        "target_grade":
            target_data,

        "minimum_score":
            minimum_data,

        "what_if":
            what_if_data
    }



# HOME PAGE


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

h1 {
    color: #be165f;
    font-size: 40px;
}

.cloud-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    max-width: 750px;
    margin: auto;
}

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

.cloud-bottom {
    position: absolute;
    width: 270px;
    height: 80px;
    left: 25px;
    top: 55px;
    background: white;
    border-radius: 60px;
    box-shadow: 0 8px 18px rgba(190,22,95,0.2);
}

.cloud-left {
    position: absolute;
    width: 100px;
    height: 100px;
    left: 55px;
    top: 10px;
    background: white;
    border-radius: 50%;
}

.cloud-right {
    position: absolute;
    width: 125px;
    height: 125px;
    right: 55px;
    top: 0;
    background: white;
    border-radius: 50%;
}

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



#1 - CALCULATE OVERALL PERFORMANCE


@app.get("/overall", response_class=HTMLResponse)
def overall():

    return """

<!DOCTYPE html>

<html>

<head>

<title>Calculate Overall Performance</title>

<style>

body {
    margin: 0;
    font-family: Arial;
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

</style>

</head>

<body>

<div class="container">

<h1>
CALCULATE OVERALL PERFORMANCE
</h1>

<div id="assessments">

<div class="assessment">

<div class="row">

<input
type="text"
class="assessment-name"
placeholder="Assessment name (optional)"
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
onclick="removeAssessment(this)"
>
REMOVE
</button>

</div>

</div>

</div>


<button
class="add-button"
onclick="addAssessment()"
>
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
onclick="window.location.href='/'"
>
BACK TO HOME
</button>

</div>


<script>

function addAssessment() {

    const assessments =
        document.getElementById("assessments");

    const newAssessment =
        document.createElement("div");

    newAssessment.className = "assessment";

    newAssessment.innerHTML = `

        <div class="row">

        <input
        type="text"
        class="assessment-name"
        placeholder="Assessment name (optional)"
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
        onclick="removeAssessment(this)"
        >
        REMOVE
        </button>

        </div>

    `;

    assessments.appendChild(newAssessment);
}


function removeAssessment(button) {

    button.closest(".assessment").remove();

}


async function calculateOverall() {

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

    let savedData = [];


    for (let i = 0; i < assessments.length; i++) {

        const assessment = assessments[i];

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


        currentEarned +=
            score * weight / 100;

        totalWeight += weight;


        savedData.push({
            name: name,
            score: score,
            weight: weight
        });

    }


    if (totalWeight > 100) {

        error.innerHTML =
            "Total assessment weight cannot be more than 100%.";

        return;
    }


    const remainingWeight =
        100 - totalWeight;


    let currentPerformance = 0;


    if (totalWeight > 0) {

        currentPerformance =
            currentEarned /
            totalWeight *
            100;

    }


    const highestFinalMark =
        Math.min(
            100,
            currentEarned + remainingWeight
        );


    // SAVE FEATURE 1

    const response =
        await fetch("/save-all", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                assessments: savedData,

                current_earned:
                    currentEarned,

                completed_weight:
                    totalWeight,

                remaining_weight:
                    remainingWeight,

                current_performance:
                    currentPerformance,

                highest_possible:
                    highestFinalMark

            })

        });


    if (!response.ok) {

        error.innerHTML =
            "Data could not be saved.";

        return;

    }


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

    <p><b>Saved successfully.</b></p>

    </div>

    `;

}


async function loadAllData() {

    const response =
        await fetch("/load-all");

    const data =
        await response.json();


    if (
        !data.assessments ||
        data.assessments.length === 0
    ) {

        return;

    }


    const container =
        document.getElementById("assessments");

    container.innerHTML = "";


    for (
        let i = 0;
        i < data.assessments.length;
        i++
    ) {

        addAssessment();

        const rows =
            document.querySelectorAll(
                ".assessment"
            );

        const row =
            rows[rows.length - 1];


        row.querySelector(
            ".assessment-name"
        ).value =
            data.assessments[i].name || "";


        row.querySelector(
            ".score"
        ).value =
            data.assessments[i].score;


        row.querySelector(
            ".weight"
        ).value =
            data.assessments[i].weight;

    }

}


window.addEventListener(
    "load",
    loadAllData
);

</script>

</body>

</html>

"""



# 2 - TARGET GRADE


@app.get("/target", response_class=HTMLResponse)
def target():

    return """

<!DOCTYPE html>

<html>

<head>

<title>Convert to Percentage & Target Grade</title>

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
    box-sizing: border-box;
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

<h1>
CONVERT TO PERCENTAGE &
SELECT A TARGET GRADE
</h1>

<div class="box">

<label>
Percentage (%)
</label>

<input
id="percentage"
type="number"
min="0"
max="100"
step="0.01"
placeholder="Enter percentage"
>

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
<option value="47">C-</option>
<option value="44">D+</option>
<option value="40">D</option>

</select>

<button onclick="showTarget()">
SHOW TARGET MARK
</button>

<div id="targetResult"></div>

<button
class="back"
onclick="window.location.href='/'"
>
BACK TO HOME
</button>

</div>

</div>


<script>

async function convertGrade() {

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


    let grade = getGrade(mark);


    document.getElementById(
        "convertResult"
    ).innerHTML = `

    <div class="result">

    <b>Letter Grade:</b>
    ${grade}

    </div>

    `;


    await fetch("/save-all", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/json"
        },

        body: JSON.stringify({

            percentage: mark,

            converted_grade: grade

        })

    });

}


async function showTarget() {

    let select =
        document.getElementById(
            "targetGrade"
        );

    let grade =
        select.options[
            select.selectedIndex
        ].text;

    let mark =
        Number(select.value);


    document.getElementById(
        "targetResult"
    ).innerHTML = `

    <div class="result">

    <b>${grade}</b>
    requires ${mark}%

    </div>

    `;


    await fetch("/save-all", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/json"
        },

        body: JSON.stringify({

            target_grade: grade

        })

    });

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
    if (mark >= 47) return "C-";
    if (mark >= 44) return "D+";
    if (mark >= 40) return "D";

    return "F";
}


async function loadAllData() {

    const response =
        await fetch("/load-all");

    const data =
        await response.json();


    if (data.target_grade) {

        document.getElementById(
            "targetGrade"
        ).value =

            data.target_grade.target_grade === "A+"
            ? 90
            : data.target_grade.target_grade === "A"
            ? 80
            : data.target_grade.target_grade === "A-"
            ? 75
            : data.target_grade.target_grade === "B+"
            ? 70
            : data.target_grade.target_grade === "B"
            ? 65
            : data.target_grade.target_grade === "B-"
            ? 60
            : data.target_grade.target_grade === "C+"
            ? 55
            : data.target_grade.target_grade === "C"
            ? 50
            : data.target_grade.target_grade === "C-"
            ? 47
            : data.target_grade.target_grade === "D+"
            ? 44
            : 40;

    }


    if (
        data.target_grade &&
        data.target_grade.percentage !== null
    ) {

        document.getElementById(
            "percentage"
        ).value =
            data.target_grade.percentage;

    }

}


window.addEventListener(
    "load",
    loadAllData
);

</script>

</body>

</html>

"""



#  3 - MINIMUM SCORE REQUIRED

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

th,
td {
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

</style>

</head>

<body>

<div class="container">

<h1>
MINIMUM SCORE REQUIRED
</h1>

<label>
Current Performance (%)
</label>

<input
type="number"
id="currentPerformance"
min="0"
max="100"
step="0.01"
placeholder="Enter"
>

<label>
Completed Weight (%)
</label>

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

<a href="/" class="back-home">
BACK TO HOME
</a>

</div>


<script>

async function calculateMinimumScore() {

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


    if (
        isNaN(currentPerformance) ||
        currentPerformance < 0 ||
        currentPerformance > 100
    ) {

        error.innerHTML =
            "Current Performance must be between 0% and 100%.";

        return;

    }


    if (
        isNaN(completedWeight) ||
        completedWeight < 0 ||
        completedWeight > 100
    ) {

        error.innerHTML =
            "Completed Weight must be between 0% and 100%.";

        return;

    }


    let currentEarned =
        currentPerformance *
        completedWeight /
        100;


    let remainingWeight =
        100 -
        completedWeight;


    let minimumScore =
        currentEarned;


    
    // CALCULATE ALL GRADE REQUIREMENTS
    
    let minimumScores = {

        "A+": calculateRequiredScore(
            90,
            currentEarned,
            remainingWeight
        ),

        "A": calculateRequiredScore(
            80,
            currentEarned,
            remainingWeight
        ),

        "A-": calculateRequiredScore(
            75,
            currentEarned,
            remainingWeight
        ),

        "B+": calculateRequiredScore(
            70,
            currentEarned,
            remainingWeight
        ),

        "B": calculateRequiredScore(
            65,
            currentEarned,
            remainingWeight
        ),

        "B-": calculateRequiredScore(
            60,
            currentEarned,
            remainingWeight
        ),

        "C+": calculateRequiredScore(
            55,
            currentEarned,
            remainingWeight
        ),

        "C": calculateRequiredScore(
            50,
            currentEarned,
            remainingWeight
        ),

        "C-": calculateRequiredScore(
            47,
            currentEarned,
            remainingWeight
        ),

        "D+": calculateRequiredScore(
            44,
            currentEarned,
            remainingWeight
        ),

        "D": calculateRequiredScore(
            40,
            currentEarned,
            remainingWeight
        )

    };


    
    // SAVE FEATURE 3
    
    const response =
        await fetch("/save-all", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                minimum_current_performance:
                    currentPerformance,

                minimum_completed_weight:
                    completedWeight,

                minimum_current_earned:
                    currentEarned,

                minimum_remaining_weight:
                    remainingWeight,

                minimum_score:
                    minimumScore,

                minimum_scores:
                    minimumScores

            })

        });


    if (!response.ok) {

        error.innerHTML =
            "Minimum Score data could not be saved.";

        return;

    }


    
    // DISPLAY
    
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

    <p>
    <strong>Data Saved Successfully.</strong>
    </p>

    </div>


    <h2>
    Grade Requirements
    </h2>


    <table>

    <tr>
    <th>Grade</th>
    <th>Final Overall Range</th>
    <th>Minimum Score Needed</th>
    </tr>


    <tr>
    <td>A+</td>
    <td>90–100</td>
    <td>${minimumScores["A+"]}</td>
    </tr>


    <tr>
    <td>A</td>
    <td>80–89</td>
    <td>${minimumScores["A"]}</td>
    </tr>


    <tr>
    <td>A-</td>
    <td>75–79</td>
    <td>${minimumScores["A-"]}</td>
    </tr>


    <tr>
    <td>B+</td>
    <td>70–74</td>
    <td>${minimumScores["B+"]}</td>
    </tr>


    <tr>
    <td>B</td>
    <td>65–69</td>
    <td>${minimumScores["B"]}</td>
    </tr>


    <tr>
    <td>B-</td>
    <td>60–64</td>
    <td>${minimumScores["B-"]}</td>
    </tr>


    <tr>
    <td>C+</td>
    <td>55–59</td>
    <td>${minimumScores["C+"]}</td>
    </tr>


    <tr>
    <td>C</td>
    <td>50–54</td>
    <td>${minimumScores["C"]}</td>
    </tr>


    <tr>
    <td>C-</td>
    <td>47–49</td>
    <td>${minimumScores["C-"]}</td>
    </tr>


    <tr>
    <td>D+</td>
    <td>44–46</td>
    <td>${minimumScores["D+"]}</td>
    </tr>


    <tr>
    <td>D</td>
    <td>40–43</td>
    <td>${minimumScores["D"]}</td>
    </tr>


    <tr>
    <td>F</td>
    <td>0–39</td>
    <td>Already Achieved</td>
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

        if (
            currentEarned >=
            minimumMark
        ) {

            return "Already Achieved";

        }

        return "Cannot Achieve";

    }


    let requiredScore =
        (
            (
                minimumMark -
                currentEarned
            )
            /
            remainingWeight
        ) * 100;


    if (requiredScore <= 0) {

        return "Already Achieved";

    }


    if (requiredScore > 100) {

        return "Cannot Achieve";

    }


    return requiredScore.toFixed(2) + "%";

}


async function loadAllData() {

    const response =
        await fetch("/load-all");

    const data =
        await response.json();


    if (!data.minimum_score) {

        return;

    }


    if (
        data.minimum_score.current_performance
        !== null &&
        data.minimum_score.current_performance
        !== undefined
    ) {

        document.getElementById(
            "currentPerformance"
        ).value =
            data.minimum_score.current_performance;

    }


    if (
        data.minimum_score.completed_weight
        !== null &&
        data.minimum_score.completed_weight
        !== undefined
    ) {

        document.getElementById(
            "completedWeight"
        ).value =
            data.minimum_score.completed_weight;

    }

}


window.addEventListener(
    "load",
    loadAllData
);

</script>

</body>

</html>

"""



#4 - WHAT-IF CALCULATOR


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
    box-sizing: border-box;
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

<h1>
WHAT-IF CALCULATOR
</h1>

<div class="box">

<label>
Current Earned (%)
</label>

<input
id="earned"
type="number"
min="0"
max="100"
step="0.01"
placeholder="Enter current earned percentage"
>


<label>
Remaining Weight (%)
</label>

<input
id="remaining"
type="number"
min="0"
max="100"
step="0.01"
placeholder="Enter remaining weight"
>


<label>
Hypothetical Score (%)
</label>

<input
id="score"
type="number"
min="0"
max="100"
step="0.01"
placeholder="Enter hypothetical score"
>


<button onclick="calculateWhatIf()">
CALCULATE
</button>


<div id="result"></div>


<button
class="back"
onclick="window.location.href='/'"
>
BACK TO HOME
</button>

</div>

</div>


<script>

async function calculateWhatIf() {

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


    // CALCULATE PROJECTED SCORE

    let projected =
        earned +
        (
            score *
            remaining /
            100
        );


    // SAVE FEATURE 4

    const response =
        await fetch("/save-all", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                earned: earned,

                remaining: remaining,

                hypothetical_score:
                    score,

                projected_score:
                    projected

            })

        });


    if (!response.ok) {

        showError(
            "What-If data could not be saved."
        );

        return;

    }


    document.getElementById(
        "result"
    ).innerHTML = `

    <div class="result">

    <b>
    Projected Overall Score:
    </b>

    <h2>
    ${projected.toFixed(2)}%
    </h2>

    <p>
    <b>Data Saved Successfully.</b>
    </p>

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


async function loadAllData() {

    const response =
        await fetch("/load-all");

    const data =
        await response.json();


    if (!data.what_if) {

        return;

    }


    if (
        data.what_if.earned !== null &&
        data.what_if.earned !== undefined
    ) {

        document.getElementById(
            "earned"
        ).value =
            data.what_if.earned;

    }


    if (
        data.what_if.remaining !== null &&
        data.what_if.remaining !== undefined
    ) {

        document.getElementById(
            "remaining"
        ).value =
            data.what_if.remaining;

    }


    if (
        data.what_if.hypothetical_score !== null &&
        data.what_if.hypothetical_score !== undefined
    ) {

        document.getElementById(
            "score"
        ).value =
            data.what_if.hypothetical_score;

    }

}


window.addEventListener(
    "load",
    loadAllData
);

</script>

</body>

</html>

"""


