# amp_viz

An experiment in producing graphviz dot files to document the subject areas in Aginity AMP. Pass the program an ODBC connection, credentials, and the metadata database name. The program scans the metadata and pulls the subject areas, dimensions, facts, reference roles, fact to dimension relationships, and fact to fact relationships. It them produces graphviz compatible dot file for each subject area and an overall version.

The dot files can be visualized using graphviz, neato is a good starting point. There's no guarantee that you'll get a readable graph, especially with the overall graph, without tweaking the settings. The subject area specific dot files are generally more readable.

Single subject area graphs take one subject area and capture every relationship one degree out. This means that fact tables and dimensions from other subject areas will be present in the graph, but only in relationship to the main subject area. I add the subject area to the dimension and fact objects if they are not in the subject area being documented.

Subject areas are green, facts are yellow, dimensions are blue.

The current code creates subject area nodes, this may not produce the best visualization in all instances. It helps anchor dimensions and facts together that may not have direct reference roles. However, these relationships aren't 'real' from a logical model standpoint. Up next I'd like to explore creating sub-graphs by subject area which may be a better solution.

### Why no pydot / pygraphviz?
A pydot refactor may be useful in the future. I'm sure the code would be cleaner / prettier, but I'm unsure about losing the fine grained control of the dot file. I'm avoiding directly integrating graphviz as dot files can be used by other tools such as Gephi. In addition, I find the process of generating a usable / readable image requires a lot of trial and error and that's easiest from the command line.

The code is not optimized, it reads everything into memory and acts against these lists. All formatting is hard-coded. The code for the overall graph versus individual subject areas is clunky and should be refactored. No warranty is expressed or implied, your mileage may vary, ask your doctor if amp_viz is right for you...

## Graph of AMP model used for Beginner Training

![ScreenShot](/student-all.png)
