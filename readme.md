# amp_viz

An experiment in producing graphviz dot files to document the subject areas in Aginity AMP. Pass the program an ODBC connection, credentials, and the metadata database name. The program scans the metadata and pulls the subject areas, dimensions, facts, reference roles, fact to dimension relationships, and fact to fact relationships. It them produces graphviz compatible dot file for each subject area and an overall version.

The dot files can be visualized using graphviz, neato is a good starting point. There's no guarantee that you'll get a readable graph, especially with the overall graph, without tweaking the settings. The subject area specific dot files are generally more readable.

Single subject area graphs take one subject area and capture every relationship one degree out. This means that fact tables and dimensions from other subject areas will be present in the graph, but only in relationship to the main subject area. I add the subject area to the dimension and fact objects if they are not in the subject area being documented.

Subject areas are green, facts are blue, dimensions are pale yellow.

The code is not optimized, it reads everything into memory and acts against these lists. All formatting is hard-coded. The code for the overall graph versus individual subject areas in clunky and should be refactored. No warranty is expressed or implied, your mileage may vary, ask your doctor if amp_viz is right for you...