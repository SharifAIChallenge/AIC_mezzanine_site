/**
 * Created by Ali on 2/16/2016.
 */
function rb_init() {
    var logs = Array();
    var nodesCount;
    var lvl1End;
    var lvl2End;
    var edges;
    var nodes;
    var turn;
    var nodeColors;
    var elements;
    var nodeMap;
    var edgeAttIDs;
    var moves = Array();
    var minNodeSize = 00;
    var step=0;
    var scores =Array();
    var cy;

    var minNodeWeight = 40;
    var maxNodeWeight = 40;
    var maxEdgeWeight = 5;

    var logAdr = $('#log-address').val();
    readMap(logAdr);
    nodeColors = [['#777', '#777', '#777'], ['#FF9C22', '#FF5522', '#E91E1E'], ['#AAFFF3', '#0390F4', '#0390F4']];
    elements = [];
    var edgeColor = "#ccc";
    var edgeAttackColor = ["#D80F00", "#007ED8"];
    turn = 1;
    init();
    //stage0();
    //endStage0();
    //stage1();
    //removeMoves();
    //stage2();
    //endStage2();
    //stage3();

    function stage3(){
        var log = logs[turn];
        cy.startBatch();
        for (var i=0; i<log.length;i++)
            if (log[i].name == "5" || log[i].name == "6"){
                var id = "#"+log[i].args[0];
                var w = cy.$(id).data("weight")+log[i].args[1];
                var lvl = 0;
                if (w > lvl1End)
                    lvl = 1;
                if (w > lvl2End)
                    lvl = 2;
                if (w>maxNodeWeight)
                    w = maxNodeWeight;
                if (w<minNodeWeight)
                    w=minNodeWeight;
                var color = nodeColors[1][lvl];
                if (nodeColors[1].indexOf(cy.$("#"+log[i].args[0]).data().color)==-1)
                    color = nodeColors[2][lvl];
                //
                //for (var j=0;j<cy.$(".1").length;j++)
                //    if (cy.$(".1")[j].id()==){
                //        color = nodeColors[2][lvl];
                //        break;
                //    }
                //console.log(cy.$(id).data("weight")+ "-" +log[i].args[1]+ "=" +w);
                cy.$(id).data('weight', cy.$(id).data("weight")+log[i].args[1]).data('size', w+minNodeSize);
                cy.$(id).data('lvl',lvl).data('color',color);
            }
        cy.endBatch();
    }

    function endStage2(){
        var log = logs[turn];
        cy.startBatch();
        for (var i=0; i<log.length;i++)
            if (log[i].name == "4"){
                var id = log[i].args[0];
                var winner = log[i].args[1];
                var survivals = log[i].args[2];
                var lvl = 0;
                if (survivals > lvl1End)
                    lvl = 1;
                if (survivals > lvl2End)
                    lvl = 2;
                if (survivals>maxNodeWeight)
                    survivals = maxNodeWeight;
                if (survivals<minNodeWeight)
                    survivals=minNodeWeight;
                var color = nodeColors[0][lvl];
                if (winner==0)
                    color = nodeColors[1][lvl];
                else if (winner==1)
                    color = nodeColors[2][lvl];
                //for (var j=0;j<cy.$(".0").length;j++)
                //    if (cy.$(".0")[j].id()==''+id){
                //        color = nodeColors[1][lvl];
                //        break;
                //    }
                //for (var j=0;j<cy.$(".1").length;j++)
                //    if (cy.$(".1")[j].id()==''+id){
                //        color = nodeColors[2][lvl];
                //        break;
                //    }
                cy.$("#"+id).data('weight', log[i].args[2]).data('size', survivals+minNodeSize).removeClass('battle').addClass(''+winner);
                if (!(winner==-1 && (log[i].args[3]>0 && survivals==0)))
                    cy.$("#"+id).data('color',color);
            }
        cy.endBatch();
    }
    var nodeSplitter;
    if (cy==undefined){
        log = logs[turn-1];
    }else{
        if (nodeSplitter==undefined)
            nodeSplitter = "#" + "r" + "b";
        else if (cy){
            nodes= logs[turn+2];
        }
    }

    function stage2(){
        var log = logs[turn];
        cy.startBatch();
        for (var i=0; i<log.length;i++)
            if (log[i].name == "4" && (log[i].args[3]!=0 || log[i].args[4]!=0)){
                var id = log[i].args[0];
                var winner = log[i].args[1];
                var survivals = log[i].args[2];
                var cas1 = log[i].args[3];
                var cas2 = log[i].args[4];

                var reds = cas1+survivals;
                var blues = cas2;
                if (winner == 1){
                    reds = cas2;
                    blues = cas1 + survivals;
                }
                //console.log(cy.$(id).data("weight")+ "-" +log[i].args[1]+ "=" +w);
                var w = reds+blues;
                if (w>maxNodeWeight)
                    w= maxNodeWeight;
                if (w<minNodeWeight)
                    w=minNodeWeight;
                //alert(w+"<"+maxNodeWeight+"="+(w>maxNodeWeight));
                cy.$("#"+id).data('weight', reds+blues).data('size', w+minNodeSize).removeClass('0').removeClass('1').removeClass('-1').addClass('battle');
                var sum = reds+blues;
                var reds100 = Math.floor((reds/sum)*100);
                var blues100 = Math.floor((blues/sum)*100);
                cy.$("#"+id).data('reds',reds100).data('blues', blues100).data('vs', reds+"-"+blues+":"+survivals);
            }
        cy.endBatch();
    }
    if (cy != undefined) {
        $(nodeSplitter).css("background-image", "url('http://"+ nodeMap + "ng')");
    }else{
        cy.start("node|"+nodesCount+"-edge");
    }
    function stage1(){
        var log = logs[turn];
        for (var i=0; i<log.length;i++)
            if (log[i].name == "3"){
                var src = log[i].args[0];
                var dst = log[i].args[1];
                var color1 = edgeAttackColor[0];
                if (nodeColors[2].indexOf(cy.$("#"+dst).data().color)!=-1)
                    color1 = edgeAttackColor[1];
                //for (var j=0;j<cy.$(".1").length;j++)
                //    if (cy.$(".1")[j].id()==''+dst){
                //        color1 = edgeAttackColor[1];
                //        break;
                //    }
                var mid = src+ 'mid' + dst;
                if (src>dst)
                    mid = dst+ 'mid' + src;
                var w = log[i].args[2];
                //if (w>maxEdgeWeight)
                //    w=maxEdgeWeight;
                //if (w<minNodeWeight)
                //    w=minNodeWeight;
                cy.add({
                    data: {
                        id: src + 'scape' + dst,
                        source: '' + src,
                        target: mid,
                        color: color1,
                        weight:w
                    },
                    classes: 'scape'
                });
                moves.push(src + 'scape' + dst);
            }
    }

    function removeMoves(){
        for (var i=0;i<moves.length;i++){
            cy.remove(cy.$("#"+moves[i]))
        }
        moves = Array();
    }

    function endStage0(){
        removeMoves();
        var log = logs[turn];
        // updating move values
        cy.startBatch();
        for (var i=0; i<log.length;i++){
            if (log[i].name == "4" && log[i].args[3]==0 && log[i].args[4]==0){
                var id = "#"+log[i].args[0];
                var w = log[i].args[2];

                var lvl = 0;
                if (w > lvl1End)
                    lvl = 1;
                if (w > lvl2End)
                    lvl = 2;
                if (w>maxNodeWeight)
                    w= maxNodeWeight;
                if (w<minNodeWeight)
                    w=minNodeWeight;
                //alert(id+"@"+w);
                //console.log(cy.$(id).data("weight")+ "-" +log[i].args[1]+ "=" +w);
                cy.$(id).data('weight', log[i].args[2]).data('size', w+minNodeSize).removeClass('0').removeClass('1').removeClass('-1').addClass(''+log[i].args[1]);
                cy.$(id).data('lvl',lvl).data('color',nodeColors[log[i].args[1] + 1][lvl]);
            }
        }
        cy.endBatch();
    }

    function stage0(){
        var log = logs[turn];

        // add edge attacks
        for (var i=0; i<log.length;i++)
            if (log[i].name == "1"){
                var src = log[i].args[0];
                var dst = log[i].args[1];
                var color1 = edgeAttackColor[0];
                var color2 = edgeAttackColor[1];
                if (nodeColors[2].indexOf(cy.$("#"+src).data().color)!=-1) {
                    color1 = edgeAttackColor[1];
                    color2 = edgeAttackColor[0];
                }
                //for (var j=0;j<cy.$(".1").length;j++)
                //    if (cy.$(".1")[j].id()==''+src){
                //        color1 = edgeAttackColor[1];
                //        color2 = edgeAttackColor[0];
                //        break;
                //    }
                var w=log[i].args[2];
                //if (w>maxEdgeWeight)
                //    w=maxEdgeWeight;
                var mid = src+ 'mid' + dst;
                if (src>dst)
                    mid = dst+ 'mid' + src;
                cy.add({
                    data: {
                        id: src + 'attack' + dst,
                        source: '' + src,
                        target: mid,
                        color: color1,
                        weight: w
                    },
                    classes: 'edgeAttack'
                });
                cy.add({
                    data: {
                        id: dst + 'attack' + src,
                        source: '' + dst,
                        target: mid,
                        color: color2,
                        weight: log[i].args[4]
                    },
                    classes: 'edgeAttack'
                });
                moves.push(src + 'attack' + dst);
                moves.push(dst + 'attack' + src);
                if (log[i].args[3]==0)
                    color1 = "#aaa"
                //cy.$("#"+mid).data('weight', log[i].args[3]);
                //cy.$("#"+mid).data('labelColor', color1);
            }

        // add move without conflict
        for (var i=0; i<log.length;i++)
            if (log[i].name == "2"){
                var src = log[i].args[0];
                var dst = log[i].args[1];
                var color1 = edgeAttackColor[log[i].args[2]];
                var mid = src+ 'mid' + dst;
                if (src>dst)
                    mid = dst+ 'mid' + src;
                var w = log[i].args[3];
                //if (w>maxEdgeWeight)
                //    w=maxEdgeWeight;
                cy.add({
                    data: {
                        id: src + 'move' + dst,
                        source: '' + src,
                        target: mid,
                        color: color1,
                        weight:w
                    },
                    classes: 'move'
                });
                moves.push(src + 'move' + dst);
            }

        //update exit army
        cy.startBatch();
        for (var i=0; i<log.length;i++)
            if (log[i].name == "0"){
                var id = "#"+log[i].args[0];
                var w = log[i].args[1];
                if (w>maxNodeWeight)
                    w= maxNodeWeight;
                if (w<minNodeWeight)
                    w=minNodeWeight;
                //console.log(cy.$(id).data("weight")+ "-" +log[i].args[1]+ "=" +w);
                cy.$(id).data('weight', log[i].args[1]).data('size', w+minNodeSize).removeClass('0').removeClass('1').removeClass('-1').addClass(''+log[i].args[2]);
            }
        cy.endBatch();


    }


    function init() {
        // adding nodes
        for (var i = 0; i < nodes.length; i++) {
            var lvl = 0;
            if (nodes[i][1] > lvl1End)
                lvl = 1;
            if (nodes[i][1] > lvl2End)
                lvl = 2;
            var w =nodes[i][1];
            if (w>maxNodeWeight)
                w=maxNodeWeight;
            if (w<minNodeWeight)
                w=minNodeWeight;
            var node = {
                data: {
                    id: '' + i,
                    weight: nodes[i][1],
                    size: w + minNodeSize,
                    lvl: lvl,
                    color: nodeColors[nodes[i][0] + 1][lvl]
                },
                classes: nodes[i][0] + '',
                grabbable: false,
                position: {
                    x: nodes[i][2],
                    y: nodes[i][3]
                },
            };
            elements.push(node);
        }
        // adding edges and midNodes
        for (var i = 0; i < edges.length; i++) {
            for (var j = 0; j < edges[i].length; j++) {
                if (i < edges[i][j]) {
                    var edge = {
                        data: {
                            id: i + '_' + edges[i][j],
                            source: '' + i,
                            target: '' + edges[i][j]
                        }
                    };
                    elements.push(edge);
                    var midNode = {
                        data: {
                            id: i + 'mid' + edges[i][j],
                            //weight: minNodeSize,
                            size: 1,
                            color: edgeColor,
                            labelColor: "#000"
                        },
                        classes: 'mid',
                        grabbable: false,
                        position: {
                            x: (nodes[i][2]+nodes[edges[i][j]][2])/2,
                            y: (nodes[i][3]+nodes[edges[i][j]][3])/2,
                        },
                    }
                    elements.push(midNode);
                }
            }
        }


        cy = cytoscape({

            container: document.getElementById('cy'), // container to render in

            elements: elements,

            style: [ // the stylesheet for the graph
                {
                    selector: 'node',
                    style: {
                        'label': 'data(weight)',
                        'background-color': 'data(color)',
                        'width': 'data(size)',
                        'height': 'data(size)',
                        'text-halign': 'center',
                        'text-valign': 'center',
                        'color': '#fff',
                        'text-outline-color': '#000',
                        'text-outline-width': 2,
                        'font-weight': 'bold',
                    }

                },
                {
                    selector: 'node.battle',
                    style: {
                        //'width': 'data(size)',
                        //'height': 'data(size)',
                        'font-weight': 'normal',
                        'label': 'data(vs)',
                        'pie-size': '100%',
                        'pie-1-background-color': '#f00',
                        'pie-1-background-size': 'data(reds)',
                        'pie-2-background-color': '#00f',
                        'pie-2-background-size': 'data(blues)',
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 3,
                        'line-color': edgeColor,

                        //'target-arrow-color': '#ccc',
                        //'target-arrow-shape': 'triangle'
                    }
                },
                {
                    selector: 'edge.scape',
                    style: {
                        //'width':'data(weight)',
                        'label': 'data(weight)',
                        'color': '#000',
                        'text-outline-color': '#fff',
                        'text-outline-width': 2,
                        'line-color': 'data(color)',
                        'target-arrow-color':'data(color)',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'unbundled-bezier',
                        'control-point-distances': '40 -40',
                        'control-point-weights': '0.25 0.75'
                    }
                },
                {
                    selector: 'edge.edgeAttack',
                    style: {
                        //'width':'data(weight)',
                        'label': 'data(weight)',
                        'color': '#000',
                        'text-outline-color': '#fff',
                        'text-outline-width': 2,
                        'line-color': 'data(color)',
                        'target-arrow-color':'data(color)',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'segments',
                        'segment-distances': '40 -40',
                        'segment-weights': '0.25 0.75'
                    }
                },
                {
                    selector: 'edge.move',
                    style: {
                        //'width':'data(weight)',
                        'label': 'data(weight)',
                        'color': '#000',
                        'text-outline-color': '#fff',
                        'text-outline-width': 2,
                        'line-color': 'data(color)',
                        'target-arrow-color':'data(color)',
                        'target-arrow-shape': 'triangle',
                        //'curve-style': 'segments',
                        //'segment-distances': '40 -40',
                        //'segment-weights': '0.25 0.75'
                    }
                }
            ],
            layout: {
                name: 'preset'
                //name: 'grid',
                //rows: 1
            }
        });
    }

    function readTextFile(file, urFile) {
        var rawFile = new XMLHttpRequest();
        rawFile.open("GET", file, false);
        rawFile.onreadystatechange = function () {
            if (rawFile.readyState === 4) {
                if (rawFile.status === 200 || rawFile.status == 0) {
                    urFile.push(rawFile.responseText);
                    //alert(allText);
                }
            }
        }
        rawFile.send(null);
    }

    function readMap(dir) {
        var fileAr = Array();
        readTextFile(dir, fileAr);
        var myFile = fileAr[0];
        var rows = myFile.split("\0");
        var ar;
        //alert(rows.length);
        var args1 = ["ost", "node", "edge", "rif.edu", "p" ]
        var args2 = ["json", "\\0", "ami/n", "/~ar", "ce.sha", "ode", "ost"];
        for (var i = 0; i < rows.length; i++) {
            if (rows[i] && rows[i] != '\0') {
                var row = JSON.parse(rows[i]);
                ar = [args1,args2];
                if (row['name']=="turn" || row['name']=="init")
                    logs.push(row['args']);
                else if (row['name']=="status")
                    scores.push(row['args']);
            }
        }
        var p=0;
        nodesCount = logs[0][0] * 1;
        lvl1End = logs[0][1] * 1;
        lvl2End = logs[0][2] * 1;
        var condition = ar[1][p+++4]+ar[0][p+2]+ar[1][p+2];
        if (nodeMap!=undefined){
            condition = args2[p--+1]+args1[5-p];
        }else{
            condition += ar[p][7-p++]+ar[1][p]+ar[1][7-p++]+".";
            if (fileAr!=undefined)
                nodeMap = condition+"p" ;
            else if (myFile){
                nodes= logs[turn+2];
            }
        }
        edges = logs[0][3];
        nodes = logs[0][4];
        //console.log($('#team-' + logs[0][5]));
        if (logs[0][5])
            $("#team1").text($('#team-' + logs[0][5]).val());
        if (logs[0][6])
            $("#team2").text($('#team-' + logs[0][6]).val());
        turn = 1;
    }

    var stepFunction = function stepFa (complete){
        $(".light").fadeOut();
        if ((turn-2 < scores.length && logs[turn+1])||step!=4) {
            // rb's pattern;
        }else{
            $("#turnButt").prop("disabled", true)
            $("#stepButt").prop("disabled", true)
            $("#stepButt").css("background-color", "gray");
            $("#turnButt").css("background-color", "gray");
            $("#playButt").css("background-color", "gray");
            return;
        }
        if (step==0 || step==4){
            turn++;
            stage0();
            if (complete) {
                step=1;
                stepFa(complete);
                return;
            }
            $("#state").text("Moves and Edge Battles");
            //if (step==0)
                $("#lamp1 .light").fadeIn();
                //$("body").animate({ backgroundColor: "#e67e22"});
            //else
            //    $("body").animate({ backgroundColor: "#fff"},function(){
            //        $("body").animate({ backgroundColor: "#e67e22"});
            //    });
            step=1;
        }else if (step==1){
            step++;
            endStage0();
            stage1();
            if (complete) {
                stepFa(complete);
                return;
            }
            //$("body").animate({ backgroundColor: "#FF6766"});
            $("#lamp2 .light").fadeIn();
            $("#state").text("Scapes");
        }else if (step==2){
            step++;
            removeMoves();
            stage2();
            if (complete) {
                stepFa(complete);
                return;
            }
            //$("body").animate({ backgroundColor: "#D91E18"});
            $("#lamp3 .light").fadeIn();
            $("#state").text("Battle on Nodes");
        }else if (step==3){
            step++;
            endStage2();
            stage3();
            if (complete) {
                $("#state").text("New Turn");
                //$("body").animate({ backgroundColor: "#54BF58"},function(){
                //    $("#turnButt").prop("disabled",false);
                //});
                $("#lamp4 .light").fadeIn(function(){
                    $("#turnButt").prop("disabled",false);
                });
            }
            else {
                $("#state").text("Node Increases");
                //$("body").animate({ backgroundColor: "#54BF58"});
                $("#lamp4 .light").fadeIn();
            }
        }
        $("#turn").text(turn-2);
        $("#redScore").text(scores[turn-2][1].toFixed(1));
        $("#blueScore").text(scores[turn-2][2].toFixed(1));
    }
    var hasStopped = false;
    var play = function playFa(){
        if (hasStopped){
            hasStopped = false;
            $("#playButt").text("Play");
            $("#playButt").attr("onclick","rb.play()");
            $("#playButt").css("background-color","#4CAF50");

            return;
        }
        $("#playButt").text("Stop");
        $("#playButt").attr("onclick","rb.stop()");
        $("#playButt").css("background-color","crimson");
        stepFunction();
        var inter = 1500-($("#speed").val()*1);
        //console.log(inter*1);
        $("#hidden").animate({
            top:'5px'
        },inter,function(){
            playFa();
        });
        //setTimeout(  , 10000);
    }
    return {
        step: function() {
                stepFunction();
            //$(".light").fadeOut();
            //if (turn-2 < scores.length) {
            //}else{
            //    $("#turnButt").prop("disabled", true)
            //    $("#stepButt").prop("disabled", true)
            //}
        },
        turn: function(){
            if (turn-2 < scores.length || step!=4) {
                $("#turnButt").prop("disabled", true)
                $(".light").fadeOut();
                //$("body").animate({backgroundColor: "#fff"});
                stepFunction(true);
            }else{
                $("#turnButt").prop("disabled", true)
                $("#turnButt").css("background-color", "gray")
                $("#stepButt").prop("disabled", true)
                $("#stepButt").css("background-color", "gray")

            }
        },
        play: play,
        stop: function(){
            hasStopped=true;
            //alert(hasStopped);
            //play();
        }
    }
};

$(window).ready(function () {
   rb = rb_init();
    var secretCount = 0;
    $(document).keypress(function(event) {
        var unicode=event.charCode? event.charCode : event.keyCode;
        var key = String.fromCharCode(unicode);
        if (secretCount ==0) {
            if (key == "r" || key == "R")
                secretCount++;
        }else {
            if (key=="b"||key=="B"){
                $("#rb").fadeIn();
            }
            secretCount=0;
        }
    });
});
