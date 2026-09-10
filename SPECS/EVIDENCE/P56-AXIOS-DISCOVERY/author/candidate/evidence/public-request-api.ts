export class Axios {
  constructor(config?: AxiosRequestConfig);
  defaults: AxiosDefaults;
  interceptors: {
    request: AxiosInterceptorManager<InternalAxiosRequestConfig>;
    response: AxiosInterceptorManager<AxiosResponse>;
  };
  getUri(config?: AxiosRequestConfig): string;
  request<T = any, R = AxiosResponseDefault, D = any, P = any>(
    config: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  get<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  delete<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  head<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  options<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  post<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  put<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  patch<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  postForm<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  putForm<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  patchForm<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  query<T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    data?: D,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
}

export interface AxiosInstance extends Axios {
  <T = any, R = AxiosResponseDefault, D = any, P = any>(
    config: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;
  <T = any, R = AxiosResponseDefault, D = any, P = any>(
    url: string,
    config?: AxiosRequestConfig<D, P>
  ): Promise<AxiosResponseResult<T, R, D, P>>;

  create(config?: CreateAxiosDefaults): AxiosInstance;
