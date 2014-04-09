/**
 * Created by Yelite on 14-4-7.
 */

/**
 * Created by Yelite on 14-3-11.
 */
function zip() {
    var args = [].slice.call(arguments);
    var shortest = args.length == 0 ? [] : args.reduce(function (a, b) {
        return a.length < b.length ? a : b
    });

    return shortest.map(function (_, i) {
        return args.map(function (array) {
            return array[i]
        })
    });
}


var data_plot;
DOM.ready(function () {
    // event binding

    var uid_select = DOM.find('#uid');
    var bid_select = DOM.find('#bid');
    var uid_filter = DOM.find('input[name=filter-uid]');
    var bid_filter = DOM.find('input[name=filter-bid]');

    var credits = {enabled: false};
    var rangeSelector = {
        buttonTheme: { // styles for the buttons
            fill: 'none',
            stroke: 'none',
            'stroke-width': 0,
            r: 4,
            style: {
                color: '#346691',
                fontWeight: 'bold'
            },
            states: {
                hover: {
                },
                select: {
                    fill: '#346691',
                    style: {
                        color: 'white'
                    }
                }
            }
        },

        buttons: [
            {
                type: 'day',
                count: 7,
                text: '1w'
            },
            {
                type: 'month',
                count: 1,
                text: '1m'
            },
            {
                type: 'all',
                text: 'All'
            }
        ],
        inputEnabled: false,
        selected: 2
    };
    var xAxis = {
        ordinal: false
    };
    var navigator = {enabled: true};

    function update_plot(data) {
        data_plot.destroy();

        var time = data.time;
        time = time.map(function (v) {
            var t = new Date(v);
            return t.getTime();
        });

        var click = data.click;
        var purchase = data.purchase;
        var save = data.save;
        var cart = data.cart;

        var series = [
            {
                name: 'click',
                type: 'spline',
                yAxis: 1,
                data: zip(time, click)
            },
            {
                name: 'purchase',
                type: 'line',
                data: zip(time, purchase)
            },
            {
                name: 'save',
                type: 'line',
                data: zip(time, save)
            },
            {
                name: 'cart',
                type: 'line',
                data: zip(time, cart)
            }
        ];
        data_plot = new Highcharts.StockChart({
            chart: {
                plotBackgroundColor: '#F5FAFF',
                borderRadius: 0,
                renderTo: 'plot'
            },
            credits: credits,
            rangeSelector: rangeSelector,
            navigator: navigator,
            title: {
                text: 'Data'
            },
            yAxis: [
                { // Primary yAxis
                    labels: {
                        style: {
                            color: '#89A54E'
                        }
                    },
                    title: {
                        style: {
                            color: '#89A54E'
                        }
                    },
                    opposite: true,
                    min: 0

                },
                { // Secondary yAxis
                    gridLineWidth: 0,
                    title: {
                        style: {
                            color: '#4572A7'
                        }
                    },
                    labels: {
                        style: {
                            color: '#4572A7'
                        }
                    },
                    min: 0
                }
            ],
            legend: {
                layout: 'vertical',
                align: 'left',
                verticalAlign: 'top',
                backgroundColor: '#FFFFFF'
            },
            series: series,
            xAxis: xAxis
        });

        data_plot.rangeSelector.render();
    }

    function create_options(list) {
        var options = DOM.create('option*' + list.length);
        list.map(function (v, i) {
            options[i].set(v);
            options[i].set('value', v);
        });
        return options;
    }

    function load_user(data) {
        var options = create_options(data.users);
        uid_select.children().remove();
        uid_select.append(options);
    }

    function load_brand(data) {
        var options = create_options(data.brands);
        bid_select.children().remove();
        bid_select.append(options);
    }

    uid_select.on('change', function (target) {
        var uid = target.get();
        data_plot.showLoading();
        XHR('get', 'user/' + uid).then(update_plot);
        XHR('get', 'user/' + uid + '/brand').then(load_brand);
    });

    bid_select.on('change', function (target) {
        var uid = uid_select.get();
        var bid = target.get();
        data_plot.showLoading();
        XHR('get', 'user/' + uid + '/brand/' + bid).then(update_plot);
    });

    XHR('get', 'user').then(load_user);

    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    data_plot = new Highcharts.StockChart({
        chart: {
            plotBackgroundColor: '#F5FAFF',
            borderRadius: 0,
            renderTo: 'plot'
        },
        credits: credits,
        rangeSelector: rangeSelector,
        navigator: navigator,
        title: {
            text: 'Data'
        },
        series: [],
        xAxis: xAxis
    });
});