/**
 * Ajax related functions, update functions required for assessment marks project
 *
 * various JavaScript utility functions required for assessment marks project
 */

//default value for theory and practical final
var thfm = 20;
var prfm = 50;

function elm(elmid) {
    return document.getElementById(elmid);
}

function fmpm() {
    var thprval = elm('thpr').value;
    //alert (thprval);
    if (thprval === "th") {
        elm('fm').value = thfm;
        elm('pm').value = thfm * 0.4;
    }
    else {
        elm('fm').value = prfm;
        elm('pm').value = prfm * 0.4;
    }
}

function yearpart() {
    var batchyear = elm('batch');
    var yeararr = ['I', 'II', 'III', 'IV'];
    //alert (np_date.year + " " +np_date.mon + " " + batchyear.value);
    if (np_date.mon >= 9 || np_date.mon <= 1) {
        elm('part').value = "I";
        if (np_date.mon >= 9) {
            if ((np_date.year - batchyear.value) >= 0 && (np_date.year - batchyear.value) < 4)
                elm('year').value = yeararr[np_date.year - batchyear.value];
        }
        else {
            if ((np_date.year - batchyear.value - 1) >= 0 && (np_date.year - batchyear.value - 1) < 4)
                elm('year').value = yeararr[np_date.year - batchyear.value - 1];
        }
    }
    else {
        elm('part').value = "II";
        if ((np_date.year - batchyear.value - 1) >= 0 && (np_date.year - batchyear.value - 1) < 4)
            elm('year').value = yeararr[np_date.year - batchyear.value - 1];
    }

}

function isempty(str) {
    var i;
    var whitesp = " \t\n\r";
    if ((str == null) || (str.length == 0))
        return true;
    var len = str.length;
    for (i = 0; i < len; i++) {
        var ch = str.charAt(i);
        if (whitesp.indexOf(ch) == -1)
            return false;
    }
    return true;
}

function isdigit(ch) {
    return ((ch >= "0") && (ch <= "9"));
}

function isinteger(str) {
    var i, ch;
    for (i = 0; i < str.length; i++) {
        ch = str.charAt(i);
        if (!isdigit(ch))
            return false;
    }
    return true;
}

function checkdate() {
    var datefield = elm('date');

    //Test for valid date
    var spregexp = /[\/-]/g; //or new RegExp("[\/-]","g");
    var datetext = datefield.value;
    var dtarr = datetext.split(spregexp);

    if (dtarr.length != 3) {
        alert("Enter valid date in 'Date' Field as 2067/11/23 or 2067-11-23");
        datefield.focus();
        return false;
    }

    for (var i = 0; i < dtarr.length; i++) {
        if (!isinteger(dtarr[i])) {
            alert("Enter valid date in 'Date' Field as 2067/11/23 or 2067-11-23");
            datefield.focus();
            return false;
        }
    }
    if (dtarr[1] > 12) {
        alert("Can we have month greater than 12, check the 'Date' Field. \n" +
            "Enter valid date in 'Date' Field as 2067/11/23 or 2067-11-23");
        datefield.focus();
        return false;
    }
    if (dtarr[2] > 32) {
        alert("Can we have date greater than 32, check the 'Date' Field. \n" +
            "Enter valid date in 'Date' Field as 2067/11/23 or 2067-11-23");
        datefield.focus();
        return false;
    }

    return true;
}

//validate form elements before submission
function validate() {
    var datefield = elm('date');
    var subfield = elm('subjects');
    var exnamefield = elm('exname');

    //Checks if fields are empty
    /*if (isempty(subfield.value)) {
        alert("Select Subject Name from 'Subject' Field");
        subfield.focus();
        return false;
    }*/
    if (isempty(datefield.value)) {
        alert("Enter valid date in 'Date' Field");
        datefield.focus();
        return false;
    }
    if (isempty(exnamefield.value)) {
        alert("Enter Examiner Name in 'Name of Examinar' Field");
        exnamefield.focus();
        return false;
    }
    if (!checkdate())
        return false;
    return true;
}

//Function to limit rows in text area
function limitrows(textarea) {
    var i;
    for (i = 0; i < 24; i++) {
        elm("m" + (i + 1)).value = "";
    }

    var textlines = textarea.value.split('\n');
    var maxrep = (textlines.length < 24) ? textlines.length : 24;
    for (i = 0; i < maxrep; i++) {
        elm("m" + (i + 1)).value = textlines[i];
    }

    if (textlines.length > 24) {
        textarea.value = textlines[0];
        for (i = 1; i < 24; ++i) {
            textarea.value += '\n' + textlines[i];
        }
    }
}

function updategroup() {
    var progval = elm('prog').value;
    var cbogroup = elm('group');
    var lastgrp;
    while (cbogroup.length > 0) {
        cbogroup.remove(0);
    }
    if (progval === 'BCE') {
        lastgrp = 8;
    } else {
        lastgrp = 2;
    }

    for (var i = 0; i < lastgrp; i++) {
        var opt = document.createElement("option");
        opt.text = String.fromCharCode(i + 'A'.charCodeAt(0));
        cbogroup.add(opt);
    }
}

//variable to hold ajax replied subjects to update subject combo
var subarr;

//Ajax functions to update the subject combo box
function roman2int(roman) {
    var txrm = ["I", "II", "III", "IV"];
    var num = 0;
    for (var i = 0; i < 4; i++) {
        if (txrm[i] === roman) {
            num = i + 1;
            break;
        }
    }
    return num;
}

function updatesubs() {
    var xhtr;
    /*if (cbo.value == "Select a Subject") {
        return;
    }*/
    var prog = elm("prog").value;
    var year = roman2int(elm("year").value);
    var part = roman2int(elm("part").value);
    xhtr = new XMLHttpRequest();
    xhtr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            //document.getElementById("jsondata").innerHTML = this.responseText;
            subarr = JSON.parse(this.responseText);
            var cbosub = elm("subjects");
            while (cbosub.length > 0) {
                cbosub.remove(0);
            }
            for (var i = 0; i < subarr.length; i++) {
                var opt = document.createElement("option");
                opt.text = subarr[i][1];
                //opt.appendChild(opt);
                cbosub.add(opt);
            }
            updatecodefmpmind(0);
        }
    };

    xhtr.open("POST", "api/get_subjects", true);
    xhtr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhtr.send("program=" + prog + "&year=" + year + "&part=" + part);
}

function updatecodefmpmind(index) {
    elm('code').value = subarr[index][0];
    thfm = subarr[index][2];
    prfm = subarr[index][3];
    fmpm();
}

function updatecodefmpm() {
    var index = elm("subjects").selectedIndex;
    updatecodefmpmind(index);
}

function updatestudents() {
    var xhtr;

    var prog = elm("prog").value;
    var batch = elm("batch").value;
    var group = elm("group").value;
    xhtr = new XMLHttpRequest();
    xhtr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var starr = JSON.parse(this.responseText);

            for (var i = 0; i < starr.length; i++) {
                elm("r" + (i + 1)).innerHTML = starr[i][0]+"/"+starr[i][1]+"/"+starr[i][2];
                elm("n" + (i + 1)).innerHTML = starr[i][3];
            }
        }
    };

    xhtr.open("POST", "api/get_students", true);
    xhtr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhtr.send("prog=" + prog + "&batch=" + batch + "&group=" + group);
}

//This code is executed after the page is completely loaded
if (document.readyState === "complete") {
    yearpart();
    updatesubs();
    updategroup();
    updatestudents();

} else {
    document.addEventListener("DOMContentLoaded", function () {
        yearpart();
        updatesubs();
        updategroup();
        updatestudents();
    });
}

