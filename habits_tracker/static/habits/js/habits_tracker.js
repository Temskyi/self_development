function update_habit(habit_id) {
    $.ajax({
        type: "GET",

        url: `update/${habit_id}/`,

        data: {
        },

        dataType: "text",

        cache: false,

        success: function (data) {
            let habit = document.querySelector(`.habit-${habit_id}`);
            let success_button = habit.querySelector('.success_button')
            let button = habit.querySelector(`.update_habit_${habit_id}`)
            if (data === "True") {
                success_button.classList.remove('btn-secondary');
                success_button.classList.add('btn-success')
                success_button.textContent = 'Завершено'
                button.classList.remove('btn-primary')
                button.classList.add('btn-warning')
                button.textContent = 'Отменить'
            } else {
                success_button.classList.remove('btn-success');
                success_button.classList.add('btn-secondary')
                success_button.textContent = 'Не завершено'
                button.classList.remove('btn-warning')
                button.classList.add('btn-primary')
                button.textContent = 'Выполнить'
            };
        }

    });

};