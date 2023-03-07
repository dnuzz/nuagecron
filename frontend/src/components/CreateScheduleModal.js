import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Input from '@mui/material/Input';

const style = {
  position: 'absolute' ,
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default function CreateScheduleModal({ api }) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [contents, setContents] = React.useState(null)
  const [fileType, setFileType] = React.useState(null)

  const fileUploaded = ( e ) => {
    e.preventDefault()
    const reader = new FileReader()
    reader.onload = async (e) => { 
      setContents(e.target.result)
    };
    reader.readAsText(e.target.files[0])
    const selectedFile = e.target.files[0]
    setFileType(selectedFile.name.split('.').pop())
  }

  return (
    <div>
      <Button onClick={handleOpen}>Create Schedule Set</Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Create a schedule set
          </Typography>
          <Input id="put-contents" maxRows="15" type="textarea" fullWidth={true} multiline={true} value={contents ? contents : ""} onChange={(e) => {setContents(e.target.value)}}/>
          <br/>
          <input
                style={{ display: "none" }}
                id="contained-button-file"
                type="file"
                onChange={(e) => fileUploaded(e)}
            />
            <label htmlFor="contained-button-file">
                <Button variant="contained" color="primary" component="span" >
                Select File
                </Button>
            </label>
            <br/>
            <Button variant="contained" disabled={contents ? false : true} color="primary" component="span" onClick={() => api.putSchedule(contents, fileType)}>
                Upload
            </Button>
        </Box>
      </Modal>
    </div>
  );
}
