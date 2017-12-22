var csrftoken = getCookie('csrftoken');
var lastChecked = null;

function load_raw() {
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date);
};

function truncate_raw() {
    var passwd = prompt("Enter Password : ", "your password here");
    if (passwd == 2011) {
        $("#cover").fadeIn(100);
        var date = $("#datepicker").val();
        $.ajax({
            type: "POST",
            url: "/tuncate_leads/",
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: "date=" + date + "&lead_type=raw_lead",
            success: function (msg) {
                $("#cover").fadeOut(100);
                alert("It's Done!");
                window.location.href=('/raw_leads/?date=' + date);
            },
            error: function(ts) {
                alert(ts.responseText)
            },
        });
    } else {
        alert('Incorrect password');
    }
};

function show (i) {
    var list_no = $("#filter_by_list_no").val();
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&pages=' + i + '&list_no=' + list_no);
};

function filter_by_list_no() {
    var list_no = $("#filter_by_list_no").val();
    var date = $("#datepicker").val();
    window.location.href=('/raw_leads/?date=' + date + '&pages=1&list_no=' + list_no);
}

function filter_by_dom() {
    var rows = $('#mytable tbody tr');
    var temp = $('#filter_by_dom').val().toLowerCase();
    var n, text;
    rows.show().filter(function() {
        text = $(this).find('td.redemption').text().toLowerCase();
        n = text.indexOf(temp);
        return n === -1;
    }).hide();
};

function find_active() {
    var date = $("#datepicker").val();
    var list_no = $("#filter_by_list_no").val();
    $("#cover").fadeIn(100);
    $.ajax({
        type: "POST",
        url: "/find_active/",
        data: "date=" + date,
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(msg){
            $("#cover").fadeOut(100);
            window.location.href=('/raw_leads/?date=' + date + '&list_no=' + list_no);
        },
        error: function(ts) {
            location.reload();
            // alert(ts.responseText)
        },
        statusCode: {
            200: function() {
                $("#cover").fadeOut(100);
                window.location.href=('/raw_leads/?date=' + date);
            },
            400: function() {
              alert('400 status code! user error, reload page');
            },
            404: function() {
              alert('404 error, reload the page');
            },
            403: function() {
              alert('403 error, reload the page');
            },
            500: function() {
              alert('500 status code! server error, reload page');
            },
            502: function() {
                alert('gateway timeout!');
            },
            504: function() {
                alert('gateway timeout!');
            }
        }
    });
};

function changestate(e) {
    var $chkboxes = $(':checkbox');

    if(e.shiftKey) {
        var start = $chkboxes.index(e.target);
        var end = $chkboxes.index(lastChecked);
        var checks = $chkboxes.slice(Math.min(start,end), Math.max(start,end)+ 1)
        checks.prop('checked', lastChecked.checked);
        var ids = [];
        for (var i = 0; i < checks.length; i += 1) {
            ids.push($(checks[i]).attr('id'))
        }
    }
    lastChecked = e.target;
};

function add_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var ids = [];
    var items = document.getElementsByClassName("r_" + name_redemption + page);

    for (i = 0; i < items.length; i += 1) {
        ids.push(items[i].id);
    };

    $.ajax({
        type: "POST",
        url: "/add_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'ids': JSON.stringify(ids),
            'redemption': name_redemption,
            'page': page,
            'date': date,
        },
        success: function (msg) {
        	for (i = 0; i < items.length; i += 1) {
    			items[i].checked = true;
        	}
            var count = $(":checkbox:checked").length;
            $("#counter").html(count);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function rem_this_name(name_redemption, page) {
    var date = $("#datepicker").val(), i;
    var ids = [];
    var items = document.getElementsByClassName("r_" + name_redemption + page);

    for (i = 0; i < items.length; i += 1) {
        ids.push(items[i].id);
    };

    $.ajax({
        type: "POST",
        url: "/rem_this_name/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'ids': JSON.stringify(ids),
            'redemption': name_redemption,
            'page': page,
            'date': date,
        },
        success: function (msg) {
            for (i = 0; i < items.length; i += 1) {
                items[i].checked = false;
            }
            var count = $(":checkbox:checked").length;
            $("#counter").html(count);
        },
        error: function(ts) {
            alert(ts.responseText)
        },
    });
};

function mark_as_good() {
    $("#cover").fadeIn(100);

    var $chkboxes = $(':checked');
    var ids = [];
    for (var i = 0; i < checks.length; i += 1) {
        ids.push($(checks[i]).attr('id'));
    }

    var name_of_campaign = prompt("Enter name of campaign : ", "your campaign name here...");

    $.ajax({
        type: "POST",
        url: "/mark_as_good/",
        data: {'ids': JSON.stringify(ids), 'name_of_campaign': name_of_campaign},
        headers: {
            'X-CSRFToken': csrftoken
        },
    });
};

function select_all() {
    $(':checkbox.lead_checkbox').prop('checked', true);
};

function un_select_all() {
    $(':checkbox.lead_checkbox').prop('checked', false);
};
