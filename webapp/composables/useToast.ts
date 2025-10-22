import { useToast } from "vue-toastification";

export const useToasts = () => {
  const toast = useToast();

  const success = (message: string) => {
    toast.success(message);
  };

  const error = (message: string) => {
    toast.error(message);
  };

  const info = (message: string) => {
    toast.info(message);
  };

  const warning = (message: string) => {
    toast.warning(message);
  };

  return {
    success,
    error,
    info,
    warning,
  };
};