import os
#import ipbd


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# Create Keys
t1w = create_key(
   'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
t2w = create_key(
   'sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')
dwi = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi')

# Field maps
b0_phase = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
b0_mag = create_key(
   'sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')
pe_rev = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_acq-multiband_dir-j_epi')

# fmri scans
rest_mb = create_key(
   'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold')
rest_sb = create_key(
   'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold')
fracback = create_key(
   'sub-{subject}/{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold')
face = create_key(
   'sub-{subject}/{session}/func/sub-{subject}_{session}_task-face_acq-singleband_bold')


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    last_run = len(seqinfo)

    info = {t1w:[], t2w:[], dwi:[], b0_phase:[],
            b0_mag:[], pe_rev:[], rest_mb:[], rest_sb:[],
            fracback:[], face:[]}

    def get_latest_series(key, s):
    #    if len(info[key]) == 0:
        info[key].append(s.series_id)
    #    else:
    #        info[key] = [s.series_id]

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        #ipdb.set_trace()
        if "mprage" in protocol:
            get_latest_series(t1w,s)
        elif "t2_sag" in protocol:
            get_latest_series(t2w,s)
        elif "b0map" in protocol and "M" in s.image_type:
            info[b0_mag].append(s.series_id)
        elif "b0map" in protocol and "P" in s.image_type:
            info[b0_phase].append(s.series_id)
        elif "topup_ref" in protocol:
            get_latest_series(pe_rev, s)
        elif "dti_multishell" in protocol and not s.is_derived:
            get_latest_series(dwi, s)
        elif "fracback" in protocol or "fracnoback" in protocol:
            get_latest_series(fracback, s)
        elif "face" in protocol:
            get_latest_series(face,s)
        elif "rest" in protocol:
            if "MB" in s.image_type:
                get_latest_series(rest_mb,s)
            else:
                get_latest_series(rest_sb,s)
        else:
            print("Series not recognized!: ", s.protocol_name, s.dcm_dir_name)
    return info

MetadataExtras = {
    b0_phase: {
        "EchoTime1": 0.00412,
        "EchoTime2": 0.00658
    }
}

IntendedFor = {
    b0_phase: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_acq-singleband_bold.nii.gz'
    ],
    b0_mag: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_acq-singleband_bold.nii.gz'
    ],
    pe_rev: [
        '{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi.nii.gz',
    ]
}

def ReplaceSubject(label):
    return label.lstrip("0")

def ReplaceSession(label):
    return label.lstrip("0")
