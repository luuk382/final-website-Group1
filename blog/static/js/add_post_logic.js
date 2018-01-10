$( document ).ready(function() {
    var ingredients = {};
    var ingredient_iterator = 0;

    $( "#button-plus" ).on( "click", function() {
        var ingredient = get_ingredients();

        ingredients[ingredient_iterator] = ingredient;
        ingredient_iterator++;

        add_ingredient_to_page(ingredient);
        get_ingredients(ingredients);
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
    }

    function get_ingredients() {
        amount = $("#ingr-amount").val();
        unit = $("#ingr-unit").val();
        description = $("#ingr-description").val();

        return {'amount': amount, 'unit': unit, 'description': description}
    };

    $("form.post-form").submit( function(eventObj) {
        $('<input />').attr('type', 'hidden')
            .attr('name', 'ingredients')
            .attr('value', JSON.stringify(ingredients))
            .appendTo('form.post-form');
        return true;
    });
});
