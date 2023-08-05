.. AUTO-GENERATED FILE -- DO NOT EDIT!

workflows.smri.freesurfer.recon
===============================


.. module:: nipype.workflows.smri.freesurfer.recon


.. _nipype.workflows.smri.freesurfer.recon.create_reconall_workflow:

:func:`create_reconall_workflow`
--------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/freesurfer/recon.py#L84>`__



Creates the ReconAll workflow in Nipype. This workflow is designed to
run the same commands as FreeSurfer's reconall script but with the added
features that a Nipype workflow provides. Before running this workflow, it
is necessary to have the FREESURFER_HOME environmental variable set to the
directory containing the version of FreeSurfer to be used in this workflow.

Example
~~~~~~~
>>> from nipype.workflows.smri.freesurfer import create_reconall_workflow
>>> recon_all = create_reconall_workflow()
>>> recon_all.inputs.inputspec.subject_id = 'subj1'
>>> recon_all.inputs.inputspec.subjects_dir = '.'
>>> recon_all.inputs.inputspec.T1_files = 'T1.nii.gz'
>>> recon_flow.run()  # doctest: +SKIP


Inputs::
       inputspec.subjects_dir : subjects directory (mandatory)
       inputspec.subject_id : name of subject (mandatory)
       inputspec.T1_files : T1 files (mandatory)
       inputspec.T2_file : T2 file (optional)
       inputspec.FLAIR_file : FLAIR file (optional)
       inputspec.cw256 : Conform inputs to 256 FOV (optional)
       inputspec.num_threads: Number of threads on nodes that utilize OpenMP (default=1)
       plugin_args : Dictionary of plugin args to set to nodes that utilize OpenMP (optional)
Outputs::
       postdatasink_outputspec.subject_id : name of the datasinked output folder in the subjects directory

Note:
The input subject_id is not passed to the commands in the workflow. Commands
that require subject_id are reading implicit inputs from
{SUBJECTS_DIR}/{subject_id}. For those commands the subject_id is set to the
default value and SUBJECTS_DIR is set to the node directory. The implicit
inputs are then copied to the node directory in order to mimic a SUBJECTS_DIR
structure. For example, if the command implicitly reads in brainmask.mgz, the
interface would copy that input file to
{node_dir}/{subject_id}/mri/brainmask.mgz and set SUBJECTS_DIR to node_dir.
The workflow only uses the input subject_id to datasink the outputs to
{subjects_dir}/{subject_id}.


Graph
~~~~~

.. graphviz::

	digraph ReconAll{

	  label="ReconAll";

	  ReconAll_inputspec[label="inputspec (utility)"];

	  ReconAll_config[label="config (utility)"];

	  ReconAll_outputspec[label="outputspec (utility)"];

	  ReconAll_PreDataSink_GetTransformPath[label="PreDataSink_GetTransformPath (utility)"];

	  ReconAll_PreDataSink_Orig[label="PreDataSink_Orig (freesurfer)"];

	  ReconAll_PreDataSink_Orig_Nu[label="PreDataSink_Orig_Nu (freesurfer)"];

	  ReconAll_PreDataSink_Nu[label="PreDataSink_Nu (freesurfer)"];

	  ReconAll_DataSink[label="DataSink (io)"];

	  ReconAll_Completion[label="Completion (utility)"];

	  ReconAll_postdatasink_outputspec[label="postdatasink_outputspec (utility)"];

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_config;

	  ReconAll_inputspec -> ReconAll_PreDataSink_GetTransformPath;

	  ReconAll_inputspec -> ReconAll_PreDataSink_GetTransformPath;

	  ReconAll_inputspec -> ReconAll_DataSink;

	  ReconAll_inputspec -> ReconAll_DataSink;

	  ReconAll_inputspec -> ReconAll_Completion;

	  subgraph cluster_ReconAll_AutoRecon1 {

	      label="AutoRecon1";

	    ReconAll_AutoRecon1_inputspec[label="inputspec (utility)"];

	    ReconAll_AutoRecon1_Check_T1s[label="Check_T1s (utility)"];

	    ReconAll_AutoRecon1_T1_prep[label="T1_prep (freesurfer)"];

	    ReconAll_AutoRecon1_Robust_Template[label="Robust_Template (utility)"];

	    ReconAll_AutoRecon1_Conform_Template[label="Conform_Template (freesurfer)"];

	    ReconAll_AutoRecon1_Bias_correction[label="Bias_correction (freesurfer)"];

	    ReconAll_AutoRecon1_Compute_Transform[label="Compute_Transform (freesurfer)"];

	    ReconAll_AutoRecon1_Copy_Transform[label="Copy_Transform (utility)"];

	    ReconAll_AutoRecon1_Check_Talairach_Alignment[label="Check_Talairach_Alignment (freesurfer)"];

	    ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu[label="Add_Transform_to_Orig_Nu (freesurfer)"];

	    ReconAll_AutoRecon1_Normalize_T1[label="Normalize_T1 (freesurfer)"];

	    ReconAll_AutoRecon1_Add_Transform_to_Orig[label="Add_Transform_to_Orig (freesurfer)"];

	    ReconAll_AutoRecon1_T2_Convert[label="T2_Convert (utility)"];

	    ReconAll_AutoRecon1_FLAIR_Convert[label="FLAIR_Convert (utility)"];

	    ReconAll_AutoRecon1_Awk[label="Awk (utility)"];

	    ReconAll_AutoRecon1_Detect_Aligment_Failures[label="Detect_Aligment_Failures (freesurfer)"];

	    ReconAll_AutoRecon1_EM_Register[label="EM_Register (freesurfer)"];

	    ReconAll_AutoRecon1_Watershed_Skull_Strip[label="Watershed_Skull_Strip (freesurfer)"];

	    ReconAll_AutoRecon1_Copy_Brainmask[label="Copy_Brainmask (utility)"];

	    ReconAll_AutoRecon1_outputspec[label="outputspec (utility)"];

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_Check_T1s;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_Check_T1s;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_T2_Convert;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_FLAIR_Convert;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_Awk;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_EM_Register;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_EM_Register;

	    ReconAll_AutoRecon1_inputspec -> ReconAll_AutoRecon1_Watershed_Skull_Strip;

	    ReconAll_AutoRecon1_Check_T1s -> ReconAll_AutoRecon1_T1_prep;

	    ReconAll_AutoRecon1_Check_T1s -> ReconAll_AutoRecon1_T1_prep;

	    ReconAll_AutoRecon1_Check_T1s -> ReconAll_AutoRecon1_Conform_Template;

	    ReconAll_AutoRecon1_Check_T1s -> ReconAll_AutoRecon1_Conform_Template;

	    ReconAll_AutoRecon1_T1_prep -> ReconAll_AutoRecon1_Robust_Template;

	    ReconAll_AutoRecon1_T1_prep -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Robust_Template -> ReconAll_AutoRecon1_Conform_Template;

	    ReconAll_AutoRecon1_Robust_Template -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Conform_Template -> ReconAll_AutoRecon1_Bias_correction;

	    ReconAll_AutoRecon1_Conform_Template -> ReconAll_AutoRecon1_Add_Transform_to_Orig;

	    ReconAll_AutoRecon1_Bias_correction -> ReconAll_AutoRecon1_Compute_Transform;

	    ReconAll_AutoRecon1_Bias_correction -> ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu;

	    ReconAll_AutoRecon1_Compute_Transform -> ReconAll_AutoRecon1_Copy_Transform;

	    ReconAll_AutoRecon1_Compute_Transform -> ReconAll_AutoRecon1_Awk;

	    ReconAll_AutoRecon1_Compute_Transform -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Copy_Transform -> ReconAll_AutoRecon1_Add_Transform_to_Orig;

	    ReconAll_AutoRecon1_Copy_Transform -> ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu;

	    ReconAll_AutoRecon1_Copy_Transform -> ReconAll_AutoRecon1_Check_Talairach_Alignment;

	    ReconAll_AutoRecon1_Copy_Transform -> ReconAll_AutoRecon1_Normalize_T1;

	    ReconAll_AutoRecon1_Copy_Transform -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu -> ReconAll_AutoRecon1_Normalize_T1;

	    ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu -> ReconAll_AutoRecon1_EM_Register;

	    ReconAll_AutoRecon1_Add_Transform_to_Orig_Nu -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Normalize_T1 -> ReconAll_AutoRecon1_Watershed_Skull_Strip;

	    ReconAll_AutoRecon1_Normalize_T1 -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Add_Transform_to_Orig -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_T2_Convert -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_FLAIR_Convert -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Awk -> ReconAll_AutoRecon1_Detect_Aligment_Failures;

	    ReconAll_AutoRecon1_EM_Register -> ReconAll_AutoRecon1_Watershed_Skull_Strip;

	    ReconAll_AutoRecon1_EM_Register -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Watershed_Skull_Strip -> ReconAll_AutoRecon1_Copy_Brainmask;

	    ReconAll_AutoRecon1_Watershed_Skull_Strip -> ReconAll_AutoRecon1_outputspec;

	    ReconAll_AutoRecon1_Copy_Brainmask -> ReconAll_AutoRecon1_outputspec;

	  }

	  subgraph cluster_ReconAll_AutoRecon2 {

	      label="AutoRecon2";

	    ReconAll_AutoRecon2_inputspec[label="inputspec (utility)"];

	    ReconAll_AutoRecon2_Intensity_Correction[label="Intensity_Correction (freesurfer)"];

	    ReconAll_AutoRecon2_Add_XForm_to_NU[label="Add_XForm_to_NU (freesurfer)"];

	    ReconAll_AutoRecon2_Align_Transform[label="Align_Transform (freesurfer)"];

	    ReconAll_AutoRecon2_CA_Normalize[label="CA_Normalize (freesurfer)"];

	    ReconAll_AutoRecon2_CA_Register[label="CA_Register (freesurfer)"];

	    ReconAll_AutoRecon2_Remove_Neck[label="Remove_Neck (freesurfer)"];

	    ReconAll_AutoRecon2_EM_Register_withSkull[label="EM_Register_withSkull (freesurfer)"];

	    ReconAll_AutoRecon2_CA_Label[label="CA_Label (freesurfer)"];

	    ReconAll_AutoRecon2_Segment_CorpusCallosum[label="Segment_CorpusCallosum (freesurfer)"];

	    ReconAll_AutoRecon2_Copy_CCSegmentation[label="Copy_CCSegmentation (utility)"];

	    ReconAll_AutoRecon2_Normalization2[label="Normalization2 (freesurfer)"];

	    ReconAll_AutoRecon2_Segment_WM[label="Segment_WM (freesurfer)"];

	    ReconAll_AutoRecon2_Edit_WhiteMatter[label="Edit_WhiteMatter (freesurfer)"];

	    ReconAll_AutoRecon2_MRI_Pretess[label="MRI_Pretess (freesurfer)"];

	    ReconAll_AutoRecon2_Fill[label="Fill (freesurfer)"];

	    ReconAll_AutoRecon2_Mask_Brain_Final_Surface[label="Mask_Brain_Final_Surface (freesurfer)"];

	    ReconAll_AutoRecon2_outputspec[label="outputspec (utility)"];

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Intensity_Correction;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Intensity_Correction;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Intensity_Correction;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Add_XForm_to_NU;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Align_Transform;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Align_Transform;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Align_Transform;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Normalize;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Normalize;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Register;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Register;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Register;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Remove_Neck;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_EM_Register_withSkull;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_EM_Register_withSkull;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Label;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_CA_Label;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Normalization2;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_Mask_Brain_Final_Surface;

	    ReconAll_AutoRecon2_Intensity_Correction -> ReconAll_AutoRecon2_Add_XForm_to_NU;

	    ReconAll_AutoRecon2_Add_XForm_to_NU -> ReconAll_AutoRecon2_Align_Transform;

	    ReconAll_AutoRecon2_Add_XForm_to_NU -> ReconAll_AutoRecon2_CA_Normalize;

	    ReconAll_AutoRecon2_Add_XForm_to_NU -> ReconAll_AutoRecon2_Remove_Neck;

	    ReconAll_AutoRecon2_Add_XForm_to_NU -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Align_Transform -> ReconAll_AutoRecon2_CA_Normalize;

	    ReconAll_AutoRecon2_Align_Transform -> ReconAll_AutoRecon2_CA_Register;

	    ReconAll_AutoRecon2_Align_Transform -> ReconAll_AutoRecon2_EM_Register_withSkull;

	    ReconAll_AutoRecon2_Align_Transform -> ReconAll_AutoRecon2_Fill;

	    ReconAll_AutoRecon2_Align_Transform -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_CA_Register;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_CA_Label;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_Segment_CorpusCallosum;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_Normalization2;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_MRI_Pretess;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_CA_Register -> ReconAll_AutoRecon2_Remove_Neck;

	    ReconAll_AutoRecon2_CA_Register -> ReconAll_AutoRecon2_CA_Label;

	    ReconAll_AutoRecon2_CA_Register -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Remove_Neck -> ReconAll_AutoRecon2_EM_Register_withSkull;

	    ReconAll_AutoRecon2_Remove_Neck -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_EM_Register_withSkull -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_CA_Label -> ReconAll_AutoRecon2_Segment_CorpusCallosum;

	    ReconAll_AutoRecon2_CA_Label -> ReconAll_AutoRecon2_Fill;

	    ReconAll_AutoRecon2_CA_Label -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Segment_CorpusCallosum -> ReconAll_AutoRecon2_Copy_CCSegmentation;

	    ReconAll_AutoRecon2_Segment_CorpusCallosum -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Segment_CorpusCallosum -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Copy_CCSegmentation -> ReconAll_AutoRecon2_Normalization2;

	    ReconAll_AutoRecon2_Copy_CCSegmentation -> ReconAll_AutoRecon2_Edit_WhiteMatter;

	    ReconAll_AutoRecon2_Copy_CCSegmentation -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_Mask_Brain_Final_Surface;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_Segment_WM;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_Edit_WhiteMatter;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Segment_WM -> ReconAll_AutoRecon2_Edit_WhiteMatter;

	    ReconAll_AutoRecon2_Segment_WM -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Edit_WhiteMatter -> ReconAll_AutoRecon2_MRI_Pretess;

	    ReconAll_AutoRecon2_Edit_WhiteMatter -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_MRI_Pretess -> ReconAll_AutoRecon2_Fill;

	    ReconAll_AutoRecon2_MRI_Pretess -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Fill -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Fill -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_Mask_Brain_Final_Surface -> ReconAll_AutoRecon2_outputspec;

	    subgraph cluster_ReconAll_AutoRecon2_AutoRecon2_Left {

	            label="AutoRecon2_Left";

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Pretess2[label="Pretess2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Tesselation[label="Tesselation (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Extract_Main_Component[label="Extract_Main_Component (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Orig[label="Copy_Orig (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth1[label="Smooth1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate1[label="inflate1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Inflate1[label="Copy_Inflate1 (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Sphere[label="Sphere (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology[label="Fix_Topology (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Euler_Number[label="Euler_Number (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Remove_Intersection[label="Remove_Intersection (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces[label="Make_Surfaces (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth2[label="Smooth2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate2[label="inflate2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature2[label="Curvature2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature1[label="Curvature1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature_Stats[label="Curvature_Stats (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Pretess2;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Pretess2;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Sphere;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Pretess2 -> ReconAll_AutoRecon2_AutoRecon2_Left_Tesselation;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Tesselation -> ReconAll_AutoRecon2_AutoRecon2_Left_Extract_Main_Component;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Orig;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Left_Smooth1;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Orig -> ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth1 -> ReconAll_AutoRecon2_AutoRecon2_Left_inflate1;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth1 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Inflate1;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Left_Sphere;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Copy_Inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Sphere -> ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Sphere -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Fix_Topology -> ReconAll_AutoRecon2_AutoRecon2_Left_Euler_Number;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Euler_Number -> ReconAll_AutoRecon2_AutoRecon2_Left_Remove_Intersection;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Remove_Intersection -> ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Remove_Intersection -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_Smooth2;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_Curvature1;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Left_inflate2;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Left_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Left_Curvature2;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Left_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature2 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature2 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature1 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature1 -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Left_Curvature_Stats -> ReconAll_AutoRecon2_AutoRecon2_Left_outputspec;

	    }

	    subgraph cluster_ReconAll_AutoRecon2_AutoRecon2_Right {

	            label="AutoRecon2_Right";

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Pretess2[label="Pretess2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Tesselation[label="Tesselation (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Extract_Main_Component[label="Extract_Main_Component (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Orig[label="Copy_Orig (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth1[label="Smooth1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate1[label="inflate1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Inflate1[label="Copy_Inflate1 (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Sphere[label="Sphere (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology[label="Fix_Topology (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Euler_Number[label="Euler_Number (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Remove_Intersection[label="Remove_Intersection (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces[label="Make_Surfaces (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth2[label="Smooth2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate2[label="inflate2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature2[label="Curvature2 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature1[label="Curvature1 (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature_Stats[label="Curvature_Stats (freesurfer)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Pretess2;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Pretess2;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Sphere;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Pretess2 -> ReconAll_AutoRecon2_AutoRecon2_Right_Tesselation;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Tesselation -> ReconAll_AutoRecon2_AutoRecon2_Right_Extract_Main_Component;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Orig;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Right_Smooth1;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Extract_Main_Component -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Orig -> ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth1 -> ReconAll_AutoRecon2_AutoRecon2_Right_inflate1;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth1 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Inflate1;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Right_Sphere;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Copy_Inflate1 -> ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Sphere -> ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Sphere -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Fix_Topology -> ReconAll_AutoRecon2_AutoRecon2_Right_Euler_Number;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Euler_Number -> ReconAll_AutoRecon2_AutoRecon2_Right_Remove_Intersection;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Remove_Intersection -> ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Remove_Intersection -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_Smooth2;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_Curvature1;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Make_Surfaces -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Right_inflate2;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Right_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Smooth2 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Right_Curvature2;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Right_Curvature_Stats;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_inflate2 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature2 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature2 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature1 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature1 -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	        ReconAll_AutoRecon2_AutoRecon2_Right_Curvature_Stats -> ReconAll_AutoRecon2_AutoRecon2_Right_outputspec;

	    }

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_inputspec -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_CA_Normalize -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_Copy_CCSegmentation -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_Copy_CCSegmentation -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_Normalization2 -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_Mask_Brain_Final_Surface -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_Mask_Brain_Final_Surface -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_MRI_Pretess -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_MRI_Pretess -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_Fill -> ReconAll_AutoRecon2_AutoRecon2_Left_inputspec;

	    ReconAll_AutoRecon2_Fill -> ReconAll_AutoRecon2_AutoRecon2_Right_inputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Left_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	    ReconAll_AutoRecon2_AutoRecon2_Right_outputspec -> ReconAll_AutoRecon2_outputspec;

	  }

	  subgraph cluster_ReconAll_AutoRecon3 {

	      label="AutoRecon3";

	    ReconAll_AutoRecon3_inputspec[label="inputspec (utility)"];

	    ReconAll_AutoRecon3_Mask_Ribbon[label="Mask_Ribbon (freesurfer)"];

	    ReconAll_AutoRecon3_Relabel_Hypointensities[label="Relabel_Hypointensities (freesurfer)"];

	    ReconAll_AutoRecon3_Aparc2Aseg[label="Aparc2Aseg (freesurfer)"];

	    ReconAll_AutoRecon3_Apas_2_Aseg[label="Apas_2_Aseg (freesurfer)"];

	    ReconAll_AutoRecon3_Aparc2Aseg_2009[label="Aparc2Aseg_2009 (freesurfer)"];

	    ReconAll_AutoRecon3_Segmentation_Statistics[label="Segmentation_Statistics (freesurfer)"];

	    ReconAll_AutoRecon3_WM_Parcellation[label="WM_Parcellation (freesurfer)"];

	    ReconAll_AutoRecon3_WM_Segmentation_Statistics[label="WM_Segmentation_Statistics (freesurfer)"];

	    ReconAll_AutoRecon3_outputspec[label="outputspec (utility)"];

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Mask_Ribbon;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Mask_Ribbon;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Mask_Ribbon;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Relabel_Hypointensities;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Relabel_Hypointensities;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Relabel_Hypointensities;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    subgraph cluster_ReconAll_AutoRecon3_AutoRecon3_Left_1 {

	            label="AutoRecon3_Left_1";

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation[label="Spherical_Inflation (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration[label="Surface_Registration (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Jacobian[label="Jacobian (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Average_Curvature[label="Average_Curvature (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation[label="Cortical_Parcellation (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface[label="Make_Pial_Surface (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Add_Pial_Area[label="Add_Pial_Area (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Mid_Pial[label="Mid_Pial (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Calculate_Volume[label="Calculate_Volume (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Jacobian;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Average_Curvature;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Add_Pial_Area;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Spherical_Inflation -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Jacobian;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Average_Curvature;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Jacobian -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Average_Curvature -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Cortical_Parcellation -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Add_Pial_Area;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Calculate_Volume;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Add_Pial_Area -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Mid_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Mid_Pial -> ReconAll_AutoRecon3_AutoRecon3_Left_1_Calculate_Volume;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Mid_Pial -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_1_Calculate_Volume -> ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec;

	    }

	    subgraph cluster_ReconAll_AutoRecon3_AutoRecon3_Right_1 {

	            label="AutoRecon3_Right_1";

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation[label="Spherical_Inflation (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration[label="Surface_Registration (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Jacobian[label="Jacobian (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Average_Curvature[label="Average_Curvature (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation[label="Cortical_Parcellation (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface[label="Make_Pial_Surface (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Add_Pial_Area[label="Add_Pial_Area (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Mid_Pial[label="Mid_Pial (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Calculate_Volume[label="Calculate_Volume (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Jacobian;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Average_Curvature;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Add_Pial_Area;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Spherical_Inflation -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Jacobian;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Average_Curvature;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Surface_Registration -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Jacobian -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Average_Curvature -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Cortical_Parcellation -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Add_Pial_Area;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Calculate_Volume;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Make_Pial_Surface -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Add_Pial_Area -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Mid_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Mid_Pial -> ReconAll_AutoRecon3_AutoRecon3_Right_1_Calculate_Volume;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Mid_Pial -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_1_Calculate_Volume -> ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec;

	    }

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_outputspec;

	    subgraph cluster_ReconAll_AutoRecon3_AutoRecon3_Left_2 {

	            label="AutoRecon3_Left_2";

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White[label="Parcellation_Stats_lh_White (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial[label="Parcellation_Stats_lh_Pial (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2[label="Cortical_Parcellation_lh_2 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2[label="Parcellation_Statistics_lh_2 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3[label="Cortical_Parcellation_lh_3 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3[label="Parcellation_Statistics_lh_3 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh[label="WM_GM_Contrast_lh (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_White -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Stats_lh_Pial -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_2 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_2 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Cortical_Parcellation_lh_3 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_Parcellation_Statistics_lh_3 -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Left_2_WM_GM_Contrast_lh -> ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec;

	    }

	    subgraph cluster_ReconAll_AutoRecon3_AutoRecon3_Right_2 {

	            label="AutoRecon3_Right_2";

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White[label="Parcellation_Stats_rh_White (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial[label="Parcellation_Stats_rh_Pial (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2[label="Cortical_Parcellation_rh_2 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2[label="Parcellation_Statistics_rh_2 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3[label="Cortical_Parcellation_rh_3 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3[label="Parcellation_Statistics_rh_3 (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh[label="WM_GM_Contrast_rh (freesurfer)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_White -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Stats_rh_Pial -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_2 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_2 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Cortical_Parcellation_rh_3 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_Parcellation_Statistics_rh_3 -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	        ReconAll_AutoRecon3_AutoRecon3_Right_2_WM_GM_Contrast_rh -> ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec;

	    }

	    ReconAll_AutoRecon3_Relabel_Hypointensities -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_Relabel_Hypointensities -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_Relabel_Hypointensities -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Aparc2Aseg -> ReconAll_AutoRecon3_Apas_2_Aseg;

	    ReconAll_AutoRecon3_Aparc2Aseg -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_Aparc2Aseg -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Apas_2_Aseg -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_Apas_2_Aseg -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_Apas_2_Aseg -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Aparc2Aseg_2009 -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Segmentation_Statistics -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_WM_Parcellation -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_WM_Parcellation -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_WM_Segmentation_Statistics -> ReconAll_AutoRecon3_outputspec;

	    subgraph cluster_ReconAll_AutoRecon3_Brodmann_Area_Maps {

	            label="Brodmann_Area_Maps";

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec[label="inputspec (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject[label="BA_Maps_lh_Thresh_srcsubject (io)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge[label="BA_Maps_lh_Thresh_Merge (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label[label="BA_Maps_lh_Thresh_Label2Label (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot[label="BA_Maps_lh_Thresh_2_Annot (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats[label="BA_Maps_lh_Thresh_Stats (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject[label="BA_Maps_lh_srcsubject (io)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge[label="BA_Maps_lh_Merge (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label[label="BA_Maps_lh_Label2Label (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot[label="BA_Maps_lh_2_Annot (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats[label="BA_Maps_lh_Stats (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject[label="BA_Maps_rh_Thresh_srcsubject (io)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge[label="BA_Maps_rh_Thresh_Merge (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label[label="BA_Maps_rh_Thresh_Label2Label (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot[label="BA_Maps_rh_Thresh_2_Annot (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats[label="BA_Maps_rh_Thresh_Stats (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject[label="BA_Maps_rh_srcsubject (io)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge[label="BA_Maps_rh_Merge (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label[label="BA_Maps_rh_Label2Label (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot[label="BA_Maps_rh_2_Annot (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats[label="BA_Maps_rh_Stats (freesurfer)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec[label="outputspec (utility)"];

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Merge -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Thresh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Merge -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_lh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Merge -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Thresh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_srcsubject -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Merge -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Label2Label -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_2_Annot -> ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	        ReconAll_AutoRecon3_Brodmann_Area_Maps_BA_Maps_rh_Stats -> ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec;

	    }

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_1_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_inputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Mask_Ribbon;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Mask_Ribbon;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Segmentation_Statistics;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_WM_Parcellation;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_WM_Segmentation_Statistics;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_1_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_AutoRecon3_Left_2_inputspec;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_AutoRecon3_Right_2_inputspec;

	    ReconAll_AutoRecon3_Mask_Ribbon -> ReconAll_AutoRecon3_Brodmann_Area_Maps_inputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Left_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_Aparc2Aseg_2009;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_AutoRecon3_Right_2_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	    ReconAll_AutoRecon3_Brodmann_Area_Maps_outputspec -> ReconAll_AutoRecon3_outputspec;

	  }

	  ReconAll_outputspec -> ReconAll_PreDataSink_Orig;

	  ReconAll_outputspec -> ReconAll_PreDataSink_Orig_Nu;

	  ReconAll_outputspec -> ReconAll_PreDataSink_Nu;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_outputspec -> ReconAll_DataSink;

	  ReconAll_PreDataSink_GetTransformPath -> ReconAll_PreDataSink_Orig;

	  ReconAll_PreDataSink_GetTransformPath -> ReconAll_PreDataSink_Orig_Nu;

	  ReconAll_PreDataSink_GetTransformPath -> ReconAll_PreDataSink_Nu;

	  ReconAll_PreDataSink_Orig -> ReconAll_DataSink;

	  ReconAll_PreDataSink_Orig_Nu -> ReconAll_DataSink;

	  ReconAll_PreDataSink_Nu -> ReconAll_DataSink;

	  ReconAll_DataSink -> ReconAll_Completion;

	  ReconAll_Completion -> ReconAll_postdatasink_outputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_inputspec -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon1_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_config -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon2_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon1_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_AutoRecon3_inputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon2_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	  ReconAll_AutoRecon3_outputspec -> ReconAll_outputspec;

	}


.. _nipype.workflows.smri.freesurfer.recon.create_skullstripped_recon_flow:

:func:`create_skullstripped_recon_flow`
---------------------------------------

`Link to code <http://github.com/nipy/nipype/tree/ec86b7476/nipype/workflows/smri/freesurfer/recon.py#L13>`__



Performs recon-all on voulmes that are already skull stripped.
FreeSurfer failes to perform skullstrippig on some volumes (especially
MP2RAGE). This can be avoided by doing skullstripping before running
recon-all (using for example SPECTRE algorithm).

Example
~~~~~~~
>>> from nipype.workflows.smri.freesurfer import create_skullstripped_recon_flow
>>> recon_flow = create_skullstripped_recon_flow()
>>> recon_flow.inputs.inputspec.subject_id = 'subj1'
>>> recon_flow.inputs.inputspec.T1_files = 'T1.nii.gz'
>>> recon_flow.run()  # doctest: +SKIP


Inputs::
       inputspec.T1_files : skullstripped T1_files (mandatory)
       inputspec.subject_id : freesurfer subject id (optional)
       inputspec.subjects_dir : freesurfer subjects directory (optional)

Outputs::

       outputspec.subject_id : freesurfer subject id
       outputspec.subjects_dir : freesurfer subjects directory


Graph
~~~~~

.. graphviz::

	digraph skullstripped_recon_all{

	  label="skullstripped_recon_all";

	  skullstripped_recon_all_inputspec[label="inputspec (utility)"];

	  skullstripped_recon_all_autorecon1[label="autorecon1 (freesurfer)"];

	  skullstripped_recon_all_link_masks[label="link_masks (utility)"];

	  skullstripped_recon_all_autorecon_resume[label="autorecon_resume (freesurfer)"];

	  skullstripped_recon_all_outputspec[label="outputspec (utility)"];

	  skullstripped_recon_all_inputspec -> skullstripped_recon_all_autorecon1;

	  skullstripped_recon_all_inputspec -> skullstripped_recon_all_autorecon1;

	  skullstripped_recon_all_inputspec -> skullstripped_recon_all_autorecon1;

	  skullstripped_recon_all_autorecon1 -> skullstripped_recon_all_link_masks;

	  skullstripped_recon_all_autorecon1 -> skullstripped_recon_all_link_masks;

	  skullstripped_recon_all_link_masks -> skullstripped_recon_all_autorecon_resume;

	  skullstripped_recon_all_link_masks -> skullstripped_recon_all_autorecon_resume;

	  skullstripped_recon_all_autorecon_resume -> skullstripped_recon_all_outputspec;

	  skullstripped_recon_all_autorecon_resume -> skullstripped_recon_all_outputspec;

	}

