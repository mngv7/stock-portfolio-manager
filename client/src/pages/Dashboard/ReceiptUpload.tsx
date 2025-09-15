import { forwardRef, useImperativeHandle, useRef, useState } from 'react';
import { FileUpload, type FileUploadSelectEvent } from 'primereact/fileupload';
import { Toast } from 'primereact/toast';
import './ReceiptUpload.css'
import { uploadReceipt, type Trade } from '../../api/portfolio';

export type ReceiptUploadHandle = {
    handleUpload: (trade: Trade) => Promise<void>;
};

const ReceiptUpload = forwardRef<ReceiptUploadHandle>((_, ref) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const toast = useRef<Toast>(null);
    const jwt = localStorage.getItem("jwt");

    const handleFileSelect = (event: FileUploadSelectEvent) => {
        setSelectedFile(event.files[0]);
    };

    useImperativeHandle(ref, () => ({
        handleUpload: async (trade: Trade) => {
            if (!jwt || !selectedFile) return;

            const response = await uploadReceipt(selectedFile, trade, jwt);
            console.log(response);
            toast.current?.show({ severity: 'success', summary: 'Uploaded', detail: selectedFile.name });

            setSelectedFile(null);
        },
    }));

    return (
        <div className="upload-card">
            <Toast ref={toast}></Toast>
            <p>Upload trade receipt</p>
            <FileUpload
                mode='basic'
                name="demo[]"
                accept="application/pdf"
                maxFileSize={1000000}
                customUpload
                onSelect={handleFileSelect}
                chooseOptions={{ label: 'Select PDF', className: 'choose-btn' }}
            />
        </div>
    );
});

export default ReceiptUpload;
