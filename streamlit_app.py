import pathlib

import numpy_financial as npf
import pandas as pd

import streamlit as st


def main():
    instructions_path = str(pathlib.Path(__file__).parent.resolve() / "instructions.md")
    readme_text = st.markdown(get_file_content_as_string(instructions_path))

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox(
        "Choose a chapter",
        ["Home", "Compounding machine", "Finance starter kit", "Investing"],
    )
    if app_mode == "Home":
        st.sidebar.success("To continue select a chapter from the toolbar.")
    elif app_mode == "Compounding machine":
        readme_text.empty()
        compounding_machine()
    elif app_mode == "Finance starter kit":
        readme_text.empty()
        finance_starter_kit()
    elif app_mode == "Investing":
        readme_text.empty()
        investing()


def compounding_machine():

    st.write('''
    # Compounding: the eighth wonder of the world

    What is compounding? Compounding is exponential increase in value due to earning interest on both the principal and the accumulated interest.

    Let's break it down quickly with an example. Let's say that you lent me $1000 for three years, and I promised to pay you 10% for each year for this favor.

    * The $1000 you loaned me is called the **principal**
    * The 10% I pay you each year is the **interest** rate on the loan

    With this arrangement, there are two ways that I might pay you back: simple interest and compound interest. In simple interest, I would simply pay you $100 (10% of $1000) at the end of each year, and return the $1000 at the end of the third year. Compound interest is more interesting. If we were to use compound interest, I would pay you 10% of the principal in the first year, then 10% of the principal *plus* the first year's interest, then 10% of the principal *plus* the first and second year's interest (and then I would also return the $1000). If you were calculating, that would be $100 in the first year (10% of $1000), $110 in the second year (10% of $1000+$100), and then $121 in the third year (10% of $1000+$100+$110).

    As a result, you would end up with $1300 with simple interest and $1331 with compound interest. It might not seem like a big difference, but if you were to change it to a 20 year loan with the same initial principal of $1000 and 10% interest, you would end up with $3000 with simple interest and $6727.50 with compound interest. As the time horizon gets longer and longer, compounding's exponential growth becomes extremely obvious.

    "Compounding is the eighth wonder of the world." This quote is often apocryphally attributed to Albert Einstein, but the misattribution should not detract from its simplicity and profoundness.

    ''')


    st.write(
    """
    ## Try it out

    Since compounding is an exponential process, it's difficult to get a handle on it unless you try some simulations. I've designed a simple tool here that will let you play with the parameters of a compounding experiment:
    * Starting principal: The amount of money you start with.
    * Years: The number of years you want to run the compounding experiment for.
    * Annual contribution: The amount you want to add to the compounding machine each year.
    * Interest rate: The amount of interest you get paid each year.

    Try extending the number of years we compound for. What happens when we contribute a small amount of money each year? And what happens to the final value when we change the interest rate around?

    """
    )

    with st.form(key="columns_in_form"):
        col1, col2 = st.beta_columns(2)
        with col1:
            principal_input = st.number_input(
                "Starting principal", min_value=0, value=1000, key="principal"
            )
            add_sum_input = st.number_input(
                "Annual contribution", min_value=0, value=0, key="add_sum"
            )
        with col2:
            years_input = st.number_input(
                "Years", min_value=0, max_value=100, value=10, key="years"
            )
            interest_rate_input = st.number_input(
                "Interest rate (%)", min_value=0, value=8, key="interest_rate"
            )
        submitted = st.form_submit_button("Run")

    future_value = npf.fv(
        rate=interest_rate_input / 100, nper=years_input, pmt=-add_sum_input, pv=-principal_input, when="begin"
    )

    st.write("You'll have this left: $", "{:,}".format(round(future_value, 2)))

    @st.cache
    def graph_compounding(years, principal, add_sum, interest_rate):
        # graphing
        year_list = []
        value = []

        for year in range(1, int(years)+1):
            principal = (principal+add_sum)*(1+interest_rate/100)
            year_list.append(year)
            value.append(principal)

        df_compounding = pd.DataFrame(zip(year_list, value), columns=['years', 'value'])
        df_compounding.index = df_compounding['years'].values
        del df_compounding['years']
        return df_compounding.round(2)

    df_compounding = graph_compounding(years_input, principal_input, add_sum_input, interest_rate_input)

    st.write("### Growth over time")

    st.bar_chart(df_compounding)

    st.write(
        '''
        It's not obvious how much compounding affects growth until we have an actual tangible demonstration like this. I understood it from a philosophical level before, but I never truly intuited and viscerally understood the power of compounding until I ran these calculations myself.

        ## Chess and compounding

        You might have heard this story before, but there is a famous legend about the origin of chess. Supposedly, when the inventor of the game showed it to the emperor of India, the emperor was so impressed by the new game that he promised any reward to the inventor.

        The inventor replied, "I only wish for this. Give me one grain of rice for the first square of the chessboard, two grains for the next square, four for the next, eight for the next, and so on for all 64 squares, with each square having double the number of grains as the square before."

        The emperor agreed, amazed that the man had asked for such a small reward — or so he thought. After a week, his treasurer came back and informed him that the reward would add up to an astronomical sum, far greater than all the rice that could conceivably be produced in many centuries!

        While this example of compounding is negative (for the king, at least), the very nature of compounding is neither good nor bad — it is simply a mathematical truth that exists. Compounding can either make or break you, but our job is to make compounding work for you in all facets of life. Harnessing compounding requires you to save or work a little bit harder today to reap a much greater reward tomorrow. Compounding is implementing delayed gratification and requires you to take a long-term view of life.

        **In sum: use your youth and long time horizon — save (but not so much that you can't enjoy the present!) and plant the seeds for your own compounding machine.** We want to look back and thank our previous selves for doing this and setting up such a practice.

        As they say, the best time to plant a tree was twenty years ago; the next best time is today.


        '''
    )

def finance_starter_kit():
    st.write('''
    # Finance starter kit

    Your financial strength is a function of four simple variables:

    1. **Income**: the money that you make
    2. **Expenses**: the money that you spend
    3. **Savings**: the pool of money you have saved
    4. **Investments**: money available for your compounding machine

    However, the first step is to understand exactly what is happening in each of these domains. Figure out how much income and expenses you have each month, and do a tally of the amount of money in your savings and investment accounts. The oft-repeated quote — What is measured is managed — is paramount here.

    Once you figure out what is going in or out of each of these buckets, I'd encourage you to think about how you might slowly begin to improve each facet. Here are some heuristics and good rules of thumb:

    ## Income

    - mostly comes from your job, and also from alternative sources (freelancing)
    - often neglected, but think about ways you can improve your income (negotiation of your salary, etc.)
    - ensure that your monthly net income (income minus expenses) is positive

    ## Expenses

    - figure out what you enjoy, and feel comfortable spending in that category (to within reason)
        - cut your expenses on everything else
    - focus your time on saving expenses on big ticket items (e.g. car payments, mortgages, subscription services, student loans)
    - other expenses: credit card debt, student loan debt, taxes
    - figure out what your average monthly expense is

    ## Savings

    - rule of thumb: your savings account should contain 3-6 months worth of expenses (computed)
        - do not put any money into investing until you have at least 3 months of savings

    ## Investments

    This is one of the most neglected parts of personal finance, yet it's arguably the most important (because this is where we get our compounding machine)!

    Go to the next section to learn more!

    ''')

def investing():

    st.write('''
    # Investing

    **Beep boop bop 🤖️ This page is currently under construction.**
    ''')

def get_file_content_as_string(path):
    with open(path, "r") as file:
        data = file.read()
    return data


if __name__ == "__main__":
    main()
