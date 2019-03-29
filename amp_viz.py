import argparse
# Standard imports
import itertools
import pyodbc

# Create dot file for all subject areas, cluster nodes by subject area
def create_dot_all_cluster (file_name, sub, dim, fct, ddr, fdr, ffr):
    # Open the output file
    f = open(file_name, 'w')

    # Start the output
    f.write('digraph amp_md { overlap=false splines=true\n\n')

    f.write('graph [fontname="Calibri" fontsize="8"];\n')
    f.write('node [fontname="Calibri" fontsize="8"];\n')
    f.write('edge [fontname="Calibri" fontsize="8"];\n\n')

    f.write("# Subject area(s)\n")
    for i,cur_sub in enumerate(sub):
        f.write('subgraph cluster_{i} {{\n'.format(i=i))
        f.write('  label="{node_title}";\n\n'.format(node_title=cur_sub[1]))  # Node name

        f.write('  #Dimensions\n')
        for cur_dimension in dim:
            if cur_dimension[3] == cur_sub[0]:
                f.write('  "{node_name}"'.format(node_name=cur_dimension[0]))  # Node name
                f.write(' [shape="box", style="filled", fillcolor="lightblue",')  # Node shape
                f.write(' label = "{node_title}"];\n'.format(node_title=cur_dimension[1]))  # Node title
        f.write('\n')

        f.write('  #Facts\n')
        for cur_fact in fct:
            if cur_fact[3] == cur_sub[0]:
                f.write('  "{node_name}"'.format(node_name=cur_fact[0]))  # Node name
                f.write(' [shape="box", style="filled", fillcolor="lightgoldenrodyellow",')  # Node shape
                f.write(' label = "{node_title}"];\n'.format(node_title=cur_fact[1]))  # Node title start
        f.write('\n')
        f.write('}\n\n')

    # Document reference roles (dim to dim)
    f.write("# Reference role(s)\n")
    for cur_ref in ddr:
        f.write('"{type_guid}" -> "{referenced_type_guid}"'.format(type_guid=cur_ref[2], referenced_type_guid=cur_ref[3]))
        f.write(' [label = "{reference_role_name}", color="blue", fontcolor="blue"];\n'.format(reference_role_name=cur_ref[1]))  # Reference role name
    f.write('\n')

    # Document fact to dimension roles
    f.write("# Fact to dimension\n")
    for cur_fk in fdr:
        f.write('"{fact_table_guid}" -> "{type_guid}"'.format(fact_table_guid=cur_fk[0], type_guid=cur_fk[2]))
        f.write(' [label = "{fact_table_name} to {type_name}", color="red", fontcolor="red"];\n'.format(fact_table_name=cur_fk[1], type_name=cur_fk[3]))  # Reference role name
    f.write('\n')

    # Document fact to fact relationships
    f.write("# Fact to fact\n")
    for cur_ff in ffr:
        f.write('"{fact_table_guid1}" -> "{fact_table_guid2}"'.format(fact_table_guid1=cur_ff[0], fact_table_guid2=cur_ff[2]))
        f.write(' [label = "{fact_table_name1} to {fact_table_name2}", color="green", fontcolor="green"];\n'.format(fact_table_name1=cur_ff[1], fact_table_name2=cur_ff[3]))  # Reference role name
    f.write('\n')

    # Finish up the output
    f.write("}" + '\n')
    f.close()

# Create dot file for all subject areas, not clustered, with nodes for each subject area and relate each fact/dim to the subject area
def create_dot_all (file_name, sub, dim, fct, ddr, fdr, ffr):
    # Open the output file
    f = open(file_name, 'w')

    # Start the output
    f.write('digraph amp_md { overlap=false splines=true\n\n')

    f.write('graph [fontname="Calibri" fontsize="8"];\n')
    f.write('node [fontname="Calibri" fontsize="8"];\n')
    f.write('edge [fontname="Calibri" fontsize="8"];\n')

    f.write("# Subject area(s)\n")
    for cur_sub in sub:
        f.write('"' + cur_sub[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="palegreen", ')  # Node shape
        f.write(' label = "{node_title}"];\n'.format(node_title=cur_sub[1]))  # Node title
    f.write('\n\n')

    f.write("# Dimension(s)\n")
    for cur_dimension in dim:
        f.write('"' + cur_dimension[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightblue"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_dimension[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_dimension[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    f.write("# Fact(s)\n")
    for cur_fact in fct:
        f.write('"' + cur_fact[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightgoldenrodyellow"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_fact[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_fact[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    # Relate dimensions to subject areas
    f.write("# Dimension to subject area\n")
    for cur_dimension in dim:
        f.write('"{type_guid}" -> "{subject_area_guid}";\n'.format(type_guid=cur_dimension[0], subject_area_guid=cur_dimension[3]))
    f.write('\n')

    # Relate facts to subject areas
    f.write("# Fact to subject area\n")
    for cur_fact in fct:
        if cur_fact[3] in sub:
            f.write('"{fact_table_guid}" -> "{subject_area_guid}";\n'.format(fact_table_guid=cur_fact[0], subject_area_guid=cur_fact[3]))
    f.write('\n')

    # Document reference roles (dim to dim)
    f.write("# Reference role(s)\n")
    for cur_ref in ddr:
        f.write('"{type_guid}" -> "{referenced_type_guid}"'.format(type_guid=cur_ref[2], referenced_type_guid=cur_ref[3]))
        f.write(' [label = "{reference_role_name}", color="blue", fontcolor="blue"];\n'.format(reference_role_name=cur_ref[1]))  # Reference role name
    f.write('\n')

    # Document fact to dimension roles
    f.write("# Fact to dimension\n")
    for cur_fk in fdr:
        f.write('"{fact_table_guid}" -> "{type_guid}"'.format(fact_table_guid=cur_fk[0], type_guid=cur_fk[2]))
        f.write(' [label = "{fact_table_name} to {type_name}", color="red", fontcolor="red"];\n'.format(fact_table_name=cur_fk[1], type_name=cur_fk[3]))  # Reference role name
    f.write('\n')

    # Document fact to fact relationships
    f.write("# Fact to fact\n")
    for cur_ff in ffr:
        f.write('"{fact_table_guid1}" -> "{fact_table_guid2}"'.format(fact_table_guid1=cur_ff[0], fact_table_guid2=cur_ff[2]))
        f.write(' [label = "{fact_table_name1} to {fact_table_name2}", color="green", fontcolor="green"];\n'.format(fact_table_name1=cur_ff[1], fact_table_name2=cur_ff[3]))  # Reference role name
    f.write('\n')

    # Finish up the output
    f.write("}" + '\n')
    f.close()


# Create dot file for all facts and dimensions in each subject area; no nodes for the subject areas
def create_dot_all_ns (file_name, sub, dim, fct, ddr, fdr, ffr):
    # Open the output file
    f = open(file_name, 'w')

    # Start the output
    f.write('digraph amp_md { overlap=false splines=true\n\n')

    f.write('graph [fontname="Calibri" fontsize="8"];\n')
    f.write('node [fontname="Calibri" fontsize="8"];\n')
    f.write('edge [fontname="Calibri" fontsize="8"];\n')

    f.write("# Dimension(s)\n")
    for cur_dimension in dim:
        f.write('"' + cur_dimension[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightblue"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_dimension[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_dimension[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    f.write("# Fact(s)\n")
    for cur_fact in fct:
        f.write('"' + cur_fact[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightgoldenrodyellow"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_fact[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_fact[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    # Document reference roles (dim to dim)
    f.write("# Reference role(s)\n")
    for cur_ref in ddr:
        f.write('"{type_guid}" -> "{referenced_type_guid}"'.format(type_guid=cur_ref[2], referenced_type_guid=cur_ref[3]))
        # f.write(' [label = "{reference_role_name}", color="blue", fontcolor="blue"];\n'.format(reference_role_name=cur_ref[1]))  # Reference role name
        f.write(' [color="blue"];\n')  # Reference role name
    f.write('\n')

    # Document fact to dimension roles
    f.write("# Fact to dimension\n")
    for cur_fk in fdr:
        f.write('"{fact_table_guid}" -> "{type_guid}"'.format(fact_table_guid=cur_fk[0], type_guid=cur_fk[2]))
        # f.write(' [label = "{fact_table_name} to {type_name}", color="red", fontcolor="red"];\n'.format(fact_table_name=cur_fk[1], type_name=cur_fk[3]))  # Reference role name
        f.write(' [color="red"];\n')  # Reference role name
    f.write('\n')

    # Document fact to fact relationships
    f.write("# Fact to fact\n")
    for cur_ff in ffr:
        f.write('"{fact_table_guid1}" -> "{fact_table_guid2}"'.format(fact_table_guid1=cur_ff[0], fact_table_guid2=cur_ff[2]))
        # f.write(' [label = "{fact_table_name1} to {fact_table_name2}", color="green", fontcolor="green"];\n'.format(fact_table_name1=cur_ff[1], fact_table_name2=cur_ff[3]))  # Reference role name
        f.write(' [color="green"];\n')  # Reference role name
    f.write('\n')

    # Finish up the output
    f.write("}" + '\n')
    f.close()


# Create a subject area specific dot file, create nodes for the related subject areas
def create_dot_sub(file_name, sub, dim, fct, ddr, fdr, ffr):
    # Open the output file
    f = open(file_name, 'w')

    # Start the output
    f.write('digraph amp_md { overlap=false splines=true')

    f.write('graph [fontname="Calibri" fontsize="8"];\n')
    f.write('node [fontname="Calibri" fontsize="8"];\n')
    f.write('edge [fontname="Calibri" fontsize="8"];\n')

    # Center diagram on the first subject area
    f.write(' root="{root_id}"'.format(root_id=sub[0]))
    f.write('\n\n')

    f.write("# Subject area(s)\n")
    f.write('"' + sub[0] + '"')  # Node name
    f.write(' [shape="box", style="filled", fillcolor="palegreen"')  # Node shape
    f.write(' label = "{node_title}"];\n'.format(node_title=sub[1]))  # Node title
    f.write('\n')

    f.write("# Dimension(s)\n")
    for cur_dimension in dim:
        f.write('"' + cur_dimension[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightblue"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_dimension[1]))  # Node title start
        if cur_dimension[3] != sub[0]:
            f.write('\\n({subject_area_id})'.format(subject_area_id=cur_dimension[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    f.write("# Fact(s)\n")
    for cur_fact in fct:
        f.write('"' + cur_fact[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightgoldenrodyellow"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_fact[1]))  # Node title start
        if cur_fact[3] != sub[0]:
            f.write('\\n({subject_area_id})'.format(subject_area_id=cur_fact[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    # Relate dimensions to subject areas
    f.write("# Dimension to subject area\n")
    for cur_dimension in dim:
        if cur_dimension[3] in sub:
            f.write('"{type_guid}" -> "{subject_area_guid}";\n'.format(type_guid=cur_dimension[0], subject_area_guid=cur_dimension[3]))
    f.write('\n')

    # Relate facts to subject areas
    f.write("# Fact to subject area\n")
    for cur_fact in fct:
        if cur_fact[3] in sub:
            f.write('"{fact_table_guid}" -> "{subject_area_guid}";\n'.format(fact_table_guid=cur_fact[0], subject_area_guid=cur_fact[3]))
    f.write('\n')

    # Document reference roles (dim to dim)
    f.write("# Reference role(s)\n")
    for cur_ref in ddr:
        f.write('"{type_guid}" -> "{referenced_type_guid}"'.format(type_guid=cur_ref[2], referenced_type_guid=cur_ref[3]))
        f.write(' [label = "{reference_role_name}", color="blue", fontcolor="blue"];\n'.format(reference_role_name=cur_ref[1]))  # Reference role name
    f.write('\n')

    # Document fact to dimension roles
    f.write("# Fact to dimension\n")
    for cur_fk in fdr:
        f.write('"{fact_table_guid}" -> "{type_guid}"'.format(fact_table_guid=cur_fk[0], type_guid=cur_fk[2]))
        f.write(' [label = "{fact_table_name} to {type_name}", color="red", fontcolor="red"];\n'.format(fact_table_name=cur_fk[1], type_name=cur_fk[3]))  # Reference role name
    f.write('\n')

    # Document fact to fact relationships
    f.write("# Fact to fact\n")
    for cur_ff in ffr:
        f.write('"{fact_table_guid1}" -> "{fact_table_guid2}"'.format(fact_table_guid1=cur_ff[0], fact_table_guid2=cur_ff[2]))
        f.write(' [label = "{fact_table_name1} to {fact_table_name2}", color="green", fontcolor="green"];\n'.format(fact_table_name1=cur_ff[1], fact_table_name2=cur_ff[3]))  # Reference role name
    f.write('\n')

    # Finish up the output
    f.write("}" + '\n')
    f.close()


# Create a subject area specific dot file, no nodes for the related subject areas
def create_dot_sub_ns(file_name, sub, dim, fct, ddr, fdr, ffr):
    # Open the output file
    f = open(file_name, 'w')

    # Start the output
    f.write('digraph amp_md { overlap=false splines=true\n\n')

    f.write('graph [fontname="Calibri" fontsize="8"];\n')
    f.write('node [fontname="Calibri" fontsize="8"];\n')
    f.write('edge [fontname="Calibri" fontsize="8"];\n\n')

    f.write("# Dimension(s)\n")
    for cur_dimension in dim:
        f.write('"' + cur_dimension[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightblue"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_dimension[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_dimension[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    f.write("# Fact(s)\n")
    for cur_fact in fct:
        f.write('"' + cur_fact[0] + '"')  # Node name
        f.write(' [shape="box", style="filled", fillcolor="lightgoldenrodyellow"')  # Node shape
        f.write(' label = "{node_title}'.format(node_title=cur_fact[1]))  # Node title start
        f.write('\\n({subject_area_id})'.format(subject_area_id=cur_fact[4]))  # Add subject area id
        f.write('"];\n')  # Close up the label
    f.write('\n')

    # Document reference roles (dim to dim)
    f.write("# Reference role(s)\n")
    for cur_ref in ddr:
        f.write('"{type_guid}" -> "{referenced_type_guid}"'.format(type_guid=cur_ref[2], referenced_type_guid=cur_ref[3]))
        #f.write(' [label = "{reference_role_name}", color="blue", fontcolor="blue"];\n'.format(reference_role_name=cur_ref[1]))  # Reference role name
        f.write(' [color="blue"];\n')  # Reference role name
    f.write('\n')

    # Document fact to dimension roles
    f.write("# Fact to dimension\n")
    for cur_fk in fdr:
        f.write('"{fact_table_guid}" -> "{type_guid}"'.format(fact_table_guid=cur_fk[0], type_guid=cur_fk[2]))
        #f.write(' [label = "{fact_table_name} to {type_name}", color="red", fontcolor="red"];\n'.format(fact_table_name=cur_fk[1], type_name=cur_fk[3]))  # Reference role name
        f.write(' [color="red"];\n')  # Reference role name
    f.write('\n')

    # Document fact to fact relationships
    f.write("# Fact to fact\n")
    for cur_ff in ffr:
        f.write('"{fact_table_guid1}" -> "{fact_table_guid2}"'.format(fact_table_guid1=cur_ff[0], fact_table_guid2=cur_ff[2]))
        #f.write(' [label = "{fact_table_name1} to {fact_table_name2}", color="green", fontcolor="green"];\n'.format(fact_table_name1=cur_ff[1], fact_table_name2=cur_ff[3]))  # Reference role name
        f.write(' [color="green"];\n')
    f.write('\n')

    # Finish up the output
    f.write("}" + '\n')
    f.close()


# Configure the argument parser
parser = argparse.ArgumentParser(prog='amp_viz', formatter_class=argparse.RawTextHelpFormatter,
                                 description='Vizualize Aginity AMP model in graphviz')
req_args = parser.add_argument_group('startup arguments')
req_args.add_argument('-c', dest="odbc_conn",
                      help="ODBC Connection name, optionally configured with name/password embedded in connection.")
req_args.add_argument('-m', dest="meta_db", help="Database schema that contains the AMP metadata.")
req_args.add_argument('-o', dest="output_file", help="Output file name")
parser.add_argument('-u', dest="user_id", default=None, help="""\
User ID for ODBC connection. Optional as many databases allow you to save the credentials in the connection.""")
parser.add_argument('-p', dest="password", default=None, help="""\
Password for ODBC connection. Optional as many databases allow you to save the credentials in the connection.""")
parms = parser.parse_args()

# Build an ODBC connection string
conn_str = 'DSN='+parms.odbc_conn
if parms.user_id is not None:
    conn_str += ';UID=' + parms.user_id
if parms.password is not None:
    conn_str += ';PWD=' + parms.password

# Establish a connection
md_conn = pyodbc.connect(conn_str, autocommit=False)
md_cur = md_conn.cursor()

# Read the subject areas
md_cur.execute("""select subject_area_guid, subject_area_name, subject_area_description
                  from {meta_db}..adf_subject_area""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_subjects = [list(x) for x in md_rows]

# Read the dimensions
md_cur.execute("""select type_guid, type_name, type_description, subject_area_guid, subject_area_id
                  from {meta_db}..adf_type aty
                  inner join {meta_db}..adf_subject_area asa using (subject_area_guid)""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_dimensions = [list(x) for x in md_rows]

# Read the fact tables
md_cur.execute("""select fact_table_guid, fact_table_name, description, subject_area_guid, subject_area_id
                  from {meta_db}..adf_fact_table aft
                  inner join {meta_db}..adf_subject_area asa using (subject_area_guid);""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_facts = [list(x) for x in md_rows]

# Dimension to dimension reference roles
md_cur.execute("""select arr.reference_role_guid, arr.reference_role_name, arr.type_guid, arr.referenced_type_guid, aty.subject_area_guid
                  from {meta_db}..adf_reference_role arr
                  inner join {meta_db}..adf_type aty using (type_guid)""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_dim_ref = [list(x) for x in md_rows]

# Fact to dimension relationships
md_cur.execute("""select fact_table_guid, fact_table_name, type_guid, type_name, aft.subject_area_guid
                  from {meta_db}..adf_fact_column afc
                  inner join {meta_db}..adf_fact_table aft using (fact_table_guid)
                  inner join {meta_db}..adf_type aty on afc.referenced_type_guid = aty.type_guid
                  where afc.column_type = 'FK'""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_fk_ref = [list(x) for x in md_rows]

# Fact to fact relationships
md_cur.execute("""select aft1.fact_table_guid, aft1.fact_table_name, aft2.fact_table_guid, aft2.fact_table_name, aft1.subject_area_guid
                  from {meta_db}..adf_fact_column afc
                  inner join {meta_db}..adf_fact_table aft1 using (fact_table_guid)
                  inner join {meta_db}..adf_fact_table aft2 on afc.referenced_fact_table_guid = aft2.fact_table_guid
                  where afc.column_type = 'FF'""".format(meta_db=parms.meta_db))
md_rows = md_cur.fetchall()
md_ff_ref = [list(x) for x in md_rows]

# Create overall graphs
create_dot_all_cluster(parms.output_file + '-all-cluster.gv', md_subjects, md_dimensions, md_facts, md_dim_ref, md_fk_ref, md_ff_ref)
create_dot_all(parms.output_file + '-all.gv', md_subjects, md_dimensions, md_facts, md_dim_ref, md_fk_ref, md_ff_ref)
create_dot_all_ns(parms.output_file + '-all-ns.gv', md_subjects, md_dimensions, md_facts, md_dim_ref, md_fk_ref, md_ff_ref)

# Loop through subject areas creating a graph for each one
for cur_sub in md_subjects:

    # Filter each list to the current subject area. Subject area guid is present in each list
    cur_dim = [dim for dim in md_dimensions if dim[3] == cur_sub[0]]
    cur_fct = [fct for fct in md_facts if fct[3] == cur_sub[0]]
    cur_ddr = [ddr for ddr in md_dim_ref if ddr[4] == cur_sub[0]]
    cur_fdr = [fdr for fdr in md_fk_ref if fdr[4] == cur_sub[0]]
    cur_ffr = [ffr for ffr in md_ff_ref if ffr[4] == cur_sub[0]]

    # Find additional dimensions that should be graphed due to reference roles
    for c in cur_ddr:
        cur_dim.append([dim for dim in md_dimensions if dim[0] == c[3]][0])

    # Find additional dimensions that should be graphed due to FD relationships
    for c in cur_fdr:
        cur_dim.append([dim for dim in md_dimensions if dim[0] == c[2]][0])

    # Find additional fact tables that should be graphed due to FF relationships
    for c in cur_ffr:
        cur_fct.append([fct for fct in md_facts if fct[0] == c[2]][0])

    # Dedup lists (list of lists so a bit tougher to dedup, use itertools)
    cur_dim.sort()
    new_dim = list(cur_dim for cur_dim,_ in itertools.groupby(cur_dim))
    cur_fct.sort()
    new_fct = list(cur_fct for cur_fct,_ in itertools.groupby(cur_fct))
    cur_ddr.sort()
    new_ddr = list(cur_ddr for cur_ddr,_ in itertools.groupby(cur_ddr))
    cur_fdr.sort()
    new_fdr = list(cur_fdr for cur_fdr,_ in itertools.groupby(cur_fdr))
    cur_fdr.sort()
    new_ffr = list(cur_ffr for cur_ffr,_ in itertools.groupby(cur_ffr))

    # Create separate dot files for each subject area
    create_dot_sub(parms.output_file + '-' + cur_sub[1] + '.gv', cur_sub, new_dim, new_fct, new_ddr, new_fdr, new_ffr)
    create_dot_sub_ns(parms.output_file + '-' + cur_sub[1] + '-ns.gv', cur_sub, new_dim, new_fct, new_ddr, new_fdr, new_ffr)

# We're done here!
md_conn.close()
exit()
