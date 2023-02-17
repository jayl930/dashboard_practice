from shiny import ui
from shiny import render
import pandas as pd
import plotnine as gg
from shiny import App

choices_role = {
    "GK": "Goal keeper",
    "DF": "Defender",
    "MF": "Midfielder",
    "ST": "Striker",
    "SUB": "Substitute",
}

choices_check = {
    "short_name": "Name",
    "age": "Age",
    "club": "Club",
    "overall": "Rating",
    "potential": "Potential",
}

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                id="x", label="Positions", choices=choices_role, selected="FW"
            ),
            ui.input_numeric(
                id="num",
                label="Maximum number of players to view",
                value=0,
                min=0,
                max=50,
            ),
            ui.panel_conditional(
                # a client-side condition for whether to display this panel
                "input.num > 0 && input.num <= 50",
                ui.input_checkbox_group(
                    id="cols",
                    label="Select which variables you want to view:",
                    choices=choices_check,
                    selected=(["short_name", "overall"]),
                ),
            ),
        ),
        ui.panel_main(
            ui.output_plot("plot"), ui.output_text("text"), ui.output_table("table")
        ),
    )
)

player = pd.read_csv("players_20.csv")
# player = player.astype({"": "object"})


def server(input, output, session):
    @output
    @render.plot
    def plot():

        plot = (
            gg.ggplot(player.overall, gg.aes(input.x(), "value", fill="variable"))
            + gg.geom_col(position="dodge")
            + gg.ylab("Overall rating")
            + gg.scale_fill_brewer(
                type="qual",
                palette="Dark2",
                name="Rating",
                labels=(["Overall", "Potential"]),
            )
            + gg.theme_classic()
        )

    @output
    @render.text
    def text():
        if input.cols() == () or input.num() <= 0 or input.num() > 50:
            return ""
        elif input.num() == 1:
            return "Display fifa20 players"
        else:
            return f"Displaying {input.num()} fifa20 players"

    @output
    @render.table
    def table():
        cols = player.filter(input.cols())
        cols.rename(
            columns={
                "short_name": "Name",
                "age": "Age",
                "club": "Club",
                "overall": "Rating",
                "potential": "Potential",
            },
            inplace=True,
        )
        pd.set_option("colheader_justify", "left")
        first_n = cols.head(input.num())
        if input.num() <= 0 or input.num() > 50:
            return None
        else:
            return first_n


app = App(app_ui, server)
