// Toast helpers — wraps react-hot-toast with themed defaults
import toast from 'react-hot-toast';

export const showSuccess = (msg: string) => toast.success(msg);
export const showError = (msg: string) => toast.error(msg);
export const showInfo = (msg: string) => toast(msg, { icon: 'ℹ️' });

export default toast;
