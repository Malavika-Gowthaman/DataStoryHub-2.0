import axiosInstance from "../plugins/axios";
import { apiConstants } from "./constants";

interface ILogin {
  username: string;
  password: string;
}

interface ILoginResponse {
  access_token: string;
  token_type: string;
}

interface ISignup extends ILogin {
  confirm_password: string;
  email: string;
}

const loginUser = async (data: ILogin): Promise<ILoginResponse> => {
  const result = await axiosInstance.post<ILoginResponse>(
    apiConstants.loginUser,
    data,
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }
  );
  const token = result?.data?.access_token || null;
  if (token) localStorage.setItem("token", token);
  return result.data;
};

const signUpUser = async (data: ISignup) => {
  return axiosInstance.post<{ msg: string }>(apiConstants.signupUser, data);
};

export class UserApi {
  loginUser = loginUser;
  signUpUser = signUpUser;
}
