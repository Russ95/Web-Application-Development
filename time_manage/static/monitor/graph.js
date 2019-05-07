var data_series = [];
var process = [];

var data_type_series = [];
var process_type = [];


var pie_series = [];

var pie_type_series = [];

var plan_series = [];
var plan = [];

var plan_type_time = [0,0,0,0,0];
var real_type_time = [0,0,0,0,0];
var type_name = ["Software_Development", "Reference", "Entertainment", "Social", "Unknown"];

$(document ).ready(function() {
    console.log( "ready!" );
    var url = window.location.pathname;
    var urlsplit = url.split("/").slice(-1)[0];
    getList(urlsplit);
    getPlan();
    setTimeout(function() {
    column_graph();
    }, 1000);
});

function getList(urlsplit) {
    $.ajax({
            url: "/time_manage/get-list-json",
            dataType : "json",
            success: updateList
    });
}

function getPlan() {
    $.ajax({
            url: "/time_manage/future_event",
            dataType : "json",
            success: updatePlan
    });
}

function updateList(items) {
    var index = 0;

    var sum = 0;
    $(items).each(function() {
            var data_line = {};
            var data_type_line = {};
            var s = String(this.fields.process_name);
            if(!process.includes(s)){
                process.push(s);
            }
            var t = String(this.fields.type);
            if(!process_type.includes(t)){
                process_type.push(t);
            }

            var d1 = new Date(this.fields.create_time);
            var d2 = new Date(this.fields.update_time);
            data_line.x = Date.UTC(d1.getUTCFullYear(), d1.getUTCMonth(), d1.getUTCDate(), d1.getUTCHours(), d1.getUTCMinutes(), d1.getUTCSeconds());
            data_line.x2 = Date.UTC(d2.getUTCFullYear(), d2.getUTCMonth(), d2.getUTCDate(), d2.getUTCHours(), d2.getUTCMinutes(), d2.getUTCSeconds());
            data_line.y = process.indexOf(String(this.fields.process_name));

            data_type_line.x = data_line.x;
            data_type_line.x2 = data_line.x2;
            data_type_line.y = process_type.indexOf(String(this.fields.type));

            data_series.push(data_line);
            data_type_series.push(data_type_line);
    });


    var pie_dict = {};
    var pie_type_dict = {};

    $(items).each(function() {

            var s = String(this.fields.process_name);
            var t = String(this.fields.type);

            var d1 = new Date(this.fields.create_time);
            var d2 = new Date(this.fields.update_time);
            var diff = d2.getTime() - d1.getTime();
            sum += diff;

            if(!process.includes(s)){
                process.push(s);
            }
            if(!process_type.includes(t)){
                process_type.push(t);
            }

            add_real_sum(t, diff/60000);

            if(pie_dict.hasOwnProperty(s)){
                pie_dict[s] = pie_dict[s] + diff;
            }else{
                pie_dict[s] = diff;
            }

            if(pie_type_dict.hasOwnProperty(t)){
                pie_type_dict[t] = pie_type_dict[t] + diff;
            }else{
                pie_type_dict[t] = diff;
            }
    });

    console.log(real_type_time);

    for (var key in pie_dict) {
        var pie_line = {};
        if (pie_dict.hasOwnProperty(key)) {
            pie_line.name = key;
            pie_line.y = pie_dict[key]

            pie_series.push(pie_line);
        }
    }

    for (var key in pie_type_dict) {
        var pie_type_line = {};
        if (pie_type_dict.hasOwnProperty(key)) {
            pie_type_line.name = key;
            pie_type_line.y = pie_type_dict[key]

            pie_type_series.push(pie_type_line);
        }
    }

    Highcharts.chart('graphcontainer', {
        chart: {
            type: 'xrange'
        },
        title: {
            text: 'history'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            categories: process,
            reversed: true
        },
        series: [{
            name: 'time tracker',
            // pointPadding: 0,
            // groupPadding: 0,
            borderColor: 'gray',
            pointWidth: 20,
            data: data_series,
            dataLabels: {
                enabled: true
            }
        }]

    });

    // Build the chart
    Highcharts.chart('piecontainer', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
      },
      title: {
        text: 'pie chart'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Brands',
        colorByPoint: true,
        data: pie_series
      }]
    });


    Highcharts.chart('graphcontainer_type', {
        chart: {
            type: 'xrange'
        },
        title: {
            text: 'history'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            categories: process_type,
            reversed: true
        },
        series: [{
            name: 'time tracker',
            // pointPadding: 0,
            // groupPadding: 0,
            borderColor: 'gray',
            pointWidth: 20,
            data: data_type_series,
            dataLabels: {
                enabled: true
            }
        }]

    });

    Highcharts.chart('piecontainer_type', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
      },
      title: {
        text: 'pie chart'
      },
      tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: 'Brands',
        colorByPoint: true,
        data: pie_type_series
      }]
    });




}


function updatePlan(items) {
    var index = 0;

    $(items).each(function() {
            //console.log(this.fields.process_name);
            var plan_line = {};
            var s = String(this.fields.title);
            if(!plan.includes(s)){
                plan.push(s);
            }
            var d1 = new Date(this.fields.start_time);
            var d2 = new Date(this.fields.end_time);
            plan_line.x = Date.UTC(d1.getUTCFullYear(), d1.getUTCMonth(), d1.getUTCDate(), d1.getUTCHours(), d1.getUTCMinutes(), d1.getUTCSeconds());
            plan_line.x2 = Date.UTC(d2.getUTCFullYear(), d2.getUTCMonth(), d2.getUTCDate(), d2.getUTCHours(), d2.getUTCMinutes(), d2.getUTCSeconds());
            plan_line.y = plan.indexOf(String(this.fields.title));

            var dif = d2-d1;
            add_plan_sum(this.fields.category, dif/60000);


            plan_series.push(plan_line);
    });
    console.log(plan_type_time);



    Highcharts.chart('plancontainer', {
        chart: {
            type: 'xrange'
        },
        title: {
            text: 'plan'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: ''
            },
            categories: plan,
            reversed: true
        },
        series: [{
            name: 'planning since today',
            // pointPadding: 0,
            // groupPadding: 0,
            borderColor: 'gray',
            pointWidth: 20,
            data: plan_series,
            dataLabels: {
                enabled: true
            }
        }]

    });

}




function add_real_sum(typename, dif){
    if(typename == type_name[0]){
        real_type_time[0] = real_type_time[0] + dif;
    }else if(typename == type_name[1]){
        real_type_time[1] = real_type_time[1] + dif;
    }else if(typename == type_name[2]){
        real_type_time[2] = real_type_time[2] + dif;
    }else if(typename == type_name[3]){
        real_type_time[3] = real_type_time[3] + dif;
    }else if(typename == type_name[4]){
        real_type_time[4] = real_type_time[4] + dif;
    }
}


function add_plan_sum(typename, dif){
    if(typename == type_name[0]){
        plan_type_time[0] = plan_type_time[0] + dif;
    }else if(typename == type_name[1]){
        plan_type_time[1] = plan_type_time[1] + dif;
    }else if(typename == type_name[2]){
        plan_type_time[2] = plan_type_time[2] + dif;
    }else if(typename == type_name[3]){
        plan_type_time[3] = plan_type_time[3] + dif;
    }else if(typename == type_name[4]){
        plan_type_time[4] = plan_type_time[4] + dif;
    }
}

function column_graph(){
    console.log(typeof(plan_type_time));
    //let result = Object.values(plan_type_time).map((e, idx) => ([++idx, e]));

    Highcharts.chart('column_container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'compare total time spend'
    },
    xAxis: {
        categories: type_name,
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'time(mins)'
        }
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'plan',
        data: plan_type_time

    }, {
        name: 'reality',
        data: real_type_time

    }]
});
}