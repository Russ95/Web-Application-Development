var plan_series = [];
var plan = [];

$(document ).ready(function() {
    console.log( "ready!" );
    getPlan();
});


function getPlan() {
    $.ajax({
            url: "/time_manage/future_event",
            dataType : "json",
            success: updatePlan
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

            plan_series.push(plan_line);
    });



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
