import numpy as np #Alle numpy functies
import matplotlib.pyplot as plt #Plotten
from scipy.optimize import curve_fit #Het effectieve fitprogramma, dit werkt met least-squares method (dus chi^2). Voor meer mogelijkheden kan later nog scipy ODR geimport worden.
from scipy.stats import chi2 #Chi^2 statistiek
import inspect #Dien om de parameter namen uit de modelfunctie te halen.

class EasyFit:
    """
    A class that contains a model for a set of data and uses this to calculate fit parameters and relevant statistics using scipy curve_fit.

    TODO:
        Add function to request figure to be able to edit the created plot.
        Add function to draw fit onto already existing figures.
    """


    def __init__(self, model: callable, graf_title: str, xdata: list, ydata: list, xlabel: str, ylabel: str, y_err: list = None, x_err: list = None, p0 = None, bounds = None) -> None:
        """
        Creates the object with a set of data and a model.

        Args:
            model (function(x, *args)): A function of x that will be used to fit to the data.
            graf_title (str): Title of the plotted graph.
            xdata (list): List of x-values for datapoints.
            ydata (list): List of y-values for datapoints.
            xlabel (str): X-axis label for the plot.
            ylabel(str): Y-axis label for the plot.
            y_err (list, optional): A list of y-value erorrs for datapoints. Defaults to None.
            x_err (list, optional): List of x-value errors fot datapoints. Defaults to None.
            p0 (list, optional): Initial guess for the fit parameters. Defaults to None
            bounds(tuple(list), optional): Bounds for the fit parameters. Defautls to None.
        """
        self.model = model
        self.graf_title = graf_title
        self.xdata = np.array(xdata) #omzetten naar np.array want veel functies doen moeilijk bij gewone python lists
        self.ydata = np.array(ydata)
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.popt = None #initialiseer alle variabelen die nog niet berekend zijn
        self.pcov = None
        self.perr = None

        self.chi2_min = None
        self.chi2_reduced = None
        self.p_value = None

        self.p0 = p0 #ken p0 en bounds toe, deze zijn ofwel None of hebben een lisjt/tuple toegekend
        self.bounds = bounds

        if y_err is None:
            self.y_err = np.array([np.abs(y)*0.01 for y in ydata]) #Default 1% error
        else:
            self.y_err = np.array(y_err)

        if x_err is None:
            self.x_err = np.array([np.abs(x)*0.01 for x in xdata]) #Default 1% error
        else:
            self.x_err = np.array(x_err)



    def __str__(self) -> str:
        """
        Prints general info to the terminal when print(object) is run.

        Returns:
            str: The final piece of string that gets printed to the terminal.
        """
        self.get_general_fit_info(interpretation=False) #print alle informatie op aparte regels
        return "\n" #een enter om te eindigen. En de functie moet iets returnen.



    def calculate_fit_parameters(self) -> None:
        """
        Calculates the optimal parameters to fit the model to the data.
        """
        
        if self.p0 is None and self.bounds is None:
            popt, pcov = curve_fit(self.model, self.xdata, self.ydata, sigma=self.y_err, absolute_sigma=True) #absolute_sigma zou ervoor zorgen dat het goed werkt met de fout

        elif self.p0 is None:
            popt, pcov = curve_fit(self.model, self.xdata, self.ydata, bounds=self.bounds, sigma=self.y_err, absolute_sigma=True)

        elif self.bounds is None:
            popt, pcov = curve_fit(self.model, self.xdata, self.ydata, p0=self.p0, sigma=self.y_err, absolute_sigma=True)
           
        else:
            popt, pcov = curve_fit(self.model, self.xdata, self.ydata, p0=self.p0, bounds=self.bounds, sigma=self.y_err, absolute_sigma=True)

        perr = np.sqrt(np.diag(pcov)) #dit is hoe de fout volgens internet berekend wordt, nog altijd niet zeker hoe dit werkt (wiskundig gezien)

        self.popt = popt
        self.pcov = pcov
        self.perr = perr



    def calculate_statistics(self) -> None:
        """
        Calculates $\chi_{min}^2$, $\chi_{red}^2$ and p-value for the fit.
        """
        residuals = self.ydata - self.model(self.xdata, *self.popt) #ik heb honestly echt mijn twijfels of deze methode uberhaupt correct is.
        chi2_min = np.sum((residuals / self.y_err)**2) #is dit een scam?

        dof = len(self.ydata) - len(self.popt) #vrijheidsgraden
        chi2_reduced = chi2_min / dof

        p_value = chi2.sf(chi2_min, dof)

        self.chi2_min = chi2_min
        self.chi2_reduced = chi2_reduced
        self.p_value = p_value



    def __print_getmethod_info__(self, getmethod_list_names: list, getmethod_names: str, combined_info: bool, statistic_values: list = None) -> None:
        """
        Structurally prints the information on either parameters or statistics.

        Args:
            getmethod_list_names (list): Names of each parameter or statistic in a list.
            getmethod_names (str): "Parameters" or "Statistics". Determines which is printed.
            combined_info (bool, optional): Passes on to the functions whether or not fit and statistic info will be printed together or not. Defaults to False
            statistic_values (list, optional): If "Statistics" were chosen, this list encompasses all the statistics. Defaults to None.

        Raises:
            ValueError: If getmethod_names does not have the value "Parameters" or "Statistics".
            Exception: If no statistic values were found. (i.e. statistic_values == None)
        """
        if not (getmethod_names == "Parameters" or getmethod_names == "Statistics"):
            raise ValueError("Parameter getmethod_names should equal \"Parameters\" or \"Statistics\".")
        
        if not combined_info:
            print('----------------------------------------------------------------------------------------------------------------')
        else:
            print()

        print(f"{getmethod_names} for fit: {self.graf_title}:\n")

        for i in range(len(getmethod_list_names)):

            if getmethod_names == "Parameters":
                print(f"Parameter {getmethod_list_names[i]}: {self.popt[i]} pm {self.perr[i]}")

            elif getmethod_names == "Statistics":

                if statistic_values == None:
                    raise Exception("No statistic values to print were found.")
                
                print(f"Statistic {getmethod_list_names[i]}: {statistic_values[i]}")
             
        if not combined_info:
            print('----------------------------------------------------------------------------------------------------------------')    



    def get_fit_parameters(self, print_values = False, combined_info = False) -> tuple:
        """
        Returns the optimized fit parameters and can print these to the terminal.

        Args:
            print_values (bool, optional): Prints information to the terminal if set to True. Defaults to False.
            combined_info (bool, optional): Passes on to the functions whether or not fit and statistic info will be printed together or not. Defaults to False

        Returns:
            tuple: A tuple containing two dictionaries. Both dictionaries have the names of the parameters as keys. The values of the first dictionary are optimized parameter values. The values of the second dictionary are errors on the parameters.
        """
        if self.popt is None:
            self.calculate_fit_parameters()

        parameter_names = inspect.getfullargspec(self.model)[0][1:] #parameter namen ophalen vanuit het model, eerste element wordt weggesliced want dit is de variabele.

        if print_values:
            self.__print_getmethod_info__(parameter_names, "Parameters", combined_info)
        
        param_dict_values = {}
        param_dict_err = {}

        for i in range(len(parameter_names)):
            param_dict_values[parameter_names[i]] = self.popt[i]
            param_dict_err[parameter_names[i]] = self.perr[i]

        return param_dict_values, param_dict_err



    def get_statistics(self, print_values=False, combined_info = False) -> dict:
        """
        Returns the statistics of the optimized fit and can print the information to the terminal.

        Args:
            print_values (bool, optional): Will print information to the terminal if set to True. Defaults to False.
            combined_info (bool, optional): Passes on to the functions whether or not fit and statistic info will be printed together or not. Defaults to False

        Returns:
            dict: A dictionary with the names of the statistics as keys and the statistic values as values.
        """
        if self.p_value is None:
            self.calculate_statistics()

        statistic_names = ["chi2_min", "chi2_red", "p-value"]
        statistics = [self.chi2_min, self.chi2_reduced, self.p_value]

        if print_values:
            self.__print_getmethod_info__(statistic_names, "Statistics", combined_info, statistics)

        statistic_dict = {}

        for i in range(len(statistic_names)):
            statistic_dict[statistic_names[i]] = statistics[i]

        return statistic_dict



    def get_general_fit_info(self, interpretation = False):
        """
        Prints all information on the fit to the terminal.

        Args:
            interpretation (bool, optional): Determines whether or not extra info about interpretation is provided. Defaults to False.
        """
        print('----------------------------------------------------------------------------------------------------------------')
        print(f"General information for the fit: {self.graf_title}:")

        _, __ = self.get_fit_parameters(print_values=True, combined_info=True)

        _ = self.get_statistics(print_values=True, combined_info=True)
        print()

        if interpretation:
            self.get_interpretaton_info(combined_info=True)
        print('----------------------------------------------------------------------------------------------------------------')



    def get_interpretaton_info(self, combined_info = False):
        """
        INFO: Provides summaries for interpreting different statistical measures, including:
        - Minimal Chi-Squared (χ²_minimal)
        - Reduced Chi-Squared (χ²_red)
        - p-value in hypothesis testing

        The function contains pre-defined summaries that explain the possible outcomes and interpretations of these statistics in a clear, step-by-step manner. 
        
        Each summary categorizes the measure into different ranges and describes the implications for each range.

        Args:
            combined_info (bool, optional): Passes on to the functions whether or not fit and statistic info will be printed together or not. Defaults to False        
        """
        chi2_minimal_summary = (
            "Interpretation of Minimal Chi-Squared (χ²_minimal):\n"
            "\t1. χ²_minimal is low:\n"
            "\t   - Suggests a good fit of the model to the data;\n"
            "\t     observed values closely match expected values.\n"
            "\t2. χ²_minimal is moderate:\n"
            "\t   - Indicates a reasonable fit;\n"
            "\t     some discrepancies between observed and expected values.\n"
            "\t3. χ²_minimal is high:\n"
            "\t   - Suggests a poor fit of the model to the data;\n"
            "\t     observed values significantly deviate from expected values."
        )
        chi_squared_summary = (
            "Interpretation of Reduced Chi-Squared (χ²_red):\n"
            "\t1. χ²_red < 1:\n"
            "\t   - Indicates that the model fits the data better than expected;\n"
            "\t     may suggest overfitting or underestimated uncertainties.\n"
            "\t2. χ²_red ≈ 1:\n"
            "\t   - Indicates a good fit; the model represents the data well.\n"
            "\t3. χ²_red > 1:\n"
            "\t   - Indicates that the model fits the data worse than expected;\n"
            "\t     may suggest significant deviations or missing factors."
        )
        p_value_summary = (
            "Interpretation of p-value using significance level α:\n"
            "\t1. P-value < α:\n"
            "\t   - Weak or no evidence in favour of the null hypothesis;\n"
            "\t     results are not statistically significant.\n"
            "\t2. P-value <≈ α:\n"
            "\t   - Weak evidence against the null hypothesis;\n"
            "\t     results may indicate a trend but are not statistically significant.\n"
            "\t3. P-value >≈ α:\n"
            "\t   - Moderate evidence in favour of the null hypothesis;\n"
            "\t     results are statistically significant but with less confidence.\n"
            "\t4. P-value > α:\n"
            "\t   - Strong evidence in favour of the null hypothesis;\n"
            "\t     results are statistically significant."
        )

        if not combined_info:
            print('----------------------------------------------------------------------------------------------------------------')

        print(chi2_minimal_summary + "\n")
        print(chi_squared_summary + "\n")
        print(p_value_summary)

        if not combined_info:
            print('----------------------------------------------------------------------------------------------------------------')



    def plot_model(self):
        """
        Plots the data points and the determined fit.
        """
        if self.popt is None:
            self.calculate_fit_parameters()

        _, ax = plt.subplots(ncols=1, nrows=1, dpi=120)

        ax.errorbar(self.xdata, self.ydata, yerr=self.y_err, xerr=self.x_err,
                    
                    label="datapunten", fmt=" ", marker="o", color="black", ecolor="black", markersize=1.5, capsize=2, capthick=0.5, elinewidth=0.5)
        #capthick = capsize/4; markersize = capsize (/2); elinewidth = capsize/4; dit moet ik mss ooit nog eens automatiseren voor mooie layout
        
        x_linspace = np.linspace(0.90*np.min(self.xdata), 1.10*np.max(self.xdata), 600)
        
        ax.plot(x_linspace, self.model(x_linspace, *self.popt),
                label="model", color="red", linestyle="--")
        
        ax.set_title(self.graf_title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        
        plt.legend()
        plt.tight_layout()
        plt.show()

    def get_all_info(self, interpretation = False):
        """
        Shows all information of the fit. Including the plotted model.

        Args:
            interpretation (bool, optional): Determines whether or not extra info about interpretation is provided. Defaults to False.
        """
        self.get_general_fit_info(interpretation)
        self.plot_model()