$( document ).ready(function() {
    var ingredients = {};
    var steps = [];
    var ingredient_iterator = 0;

    $( "#button-plus" ).on( "click", function() {
        var ingredient = get_ingredients();

        ingredients[ingredient_iterator] = ingredient;
        ingredient_iterator++;

        add_ingredient_to_page(ingredient);
    });

    $( "#button-plus2" ).on( "click", function() {
        var step = get_steps();
        steps.push(step);

        add_step_to_page(step);
    });

    function add_ingredient_to_page(ingredient) {
        $('#ingredient-table tr:last').after(
            "<tr id=\"ingredient_nr_" + ingredient_iterator + "\"><td>" + ingredient["amount"] + "</td>" +
            "<td>" + ingredient["unit"] + "</td>" +
            "<td>" + ingredient["description"] + "</td>" +
            "<td>" + "<div class=\"button-minus\"></div></td></tr>"
        );

        $( ".button-minus" ).on( "click", function() {
            var current_tr = $(this).parent().parent();
            var tr_id = current_tr.attr("id");
            var clicked_ing = tr_id.split("_")[2]
            ingredients[parseInt(clicked_ing)] = "";

            current_tr.remove();
        });
      };

      function add_step_to_page(step) {
        $('#step-table tr:last').after(
            "<tr id=\"step_nr_" + steps.length + "\"><td>" + steps[steps.length - 1] + "</td>" +
            "<td>" + "<div class=\"button-minus2\"></div></td></tr>"
        );

        $( ".button-minus2" ).on( "click", function() {
            var current_tr = $(this).parent().parent();
            var tr_id = current_tr.attr("id");
            var clicked_step = tr_id.split("_")[2]
            steps.pop()

            current_tr.remove();
       });
     };

    function get_ingredients() {
        amount = $("#ingr-amount").val();
        unit = $("#ingr-unit").val();
        description = $("#ingr-description").val();

        return {'amount': amount, 'unit': unit, 'description': description}
    };

    function get_steps() {
        step_info = $("#step-descr").val();
        return (step_info)
    };


    $("form.post-form").submit( function(eventObj) {
        $('<input />').attr('type', 'hidden')
            .attr('name', 'ingredients')
            .attr('value', JSON.stringify(ingredients))
            .appendTo('form.post-form');

        $('<input />').attr('type', 'hidden')
            .attr('name', 'steps')
            .attr('value', JSON.stringify(steps))
            .appendTo('form.post-form');
        return true;
    });
});