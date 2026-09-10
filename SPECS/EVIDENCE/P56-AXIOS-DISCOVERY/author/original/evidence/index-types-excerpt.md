export interface LookupAddressEntry {
  address: string;
  family?: AddressFamily;
}

export type LookupAddress = string | LookupAddressEntry;

export interface AxiosRequestConfig<D = any, P = any> {
  url?: string;
  method?: StringLiteralsOrString<Method>;
  baseURL?: string;
  allowAbsoluteUrls?: boolean;
  transformRequest?: AxiosRequestTransformer | AxiosRequestTransformer[];
  transformResponse?: AxiosResponseTransformer | AxiosResponseTransformer[];
  headers?: (RawAxiosRequestHeaders & MethodsHeaders) | AxiosHeaders;
  params?: P;
  paramsSerializer?:
    | ParamsSerializerOptions<unknown extends P ? Record<string, any> : P>
    | CustomParamsSerializer<unknown extends P ? Record<string, any> : P>;
  data?: D;
  timeout?: Milliseconds;
  timeoutErrorMessage?: string;
  withCredentials?: boolean;
  adapter?: AxiosAdapterConfig | AxiosAdapterConfig[];
  auth?: AxiosBasicCredentials;
  responseType?: ResponseType;
  responseEncoding?: StringLiteralsOrString<responseEncoding>;
  xsrfCookieName?: string;
  xsrfHeaderName?: string;
  onUploadProgress?: (progressEvent: AxiosProgressEvent) => void;
  onDownloadProgress?: (progressEvent: AxiosProgressEvent) => void;
  maxContentLength?: number;
  validateStatus?: ((status: number) => boolean) | null;
  maxBodyLength?: number;
  maxRedirects?: number;
  maxRate?: number | [MaxUploadRate, MaxDownloadRate];
  beforeRedirect?: (
    options: Record<string, any>,
    responseDetails: {
      headers: Record<string, string>;
      statusCode: HttpStatusCode;
    },
    requestDetails: {
      headers: Record<string, string>;
      url: string;
      method: string;
    },
  ) => void;
  socketPath?: string | null;
  allowedSocketPaths?: string | string[] | null;
  transport?: any;
  httpAgent?: any;
  httpsAgent?: any;
  proxy?: AxiosProxyConfig | false;
  cancelToken?: CancelToken | undefined;
  decompress?: boolean;
  transitional?: TransitionalOptions;
  signal?: GenericAbortSignal;
  insecureHTTPParser?: boolean;
  env?: {
    FormData?: new (...args: any[]) => object;
    fetch?: (input: URL | Request | string, init?: RequestInit) => Promise<Response>;
    Request?: new (input: URL | Request | string, init?: RequestInit) => Request;
    Response?: new (
      body?: ArrayBuffer | ArrayBufferView | Blob | FormData | URLSearchParams | string | null,
      init?: ResponseInit
    ) => Response;
  };
  formSerializer?: FormSerializerOptions;
  family?: AddressFamily;
  lookup?:
    | ((
        hostname: string,
        options: object,
        cb: (
          err: Error | null,
          address: LookupAddress | LookupAddress[],
          family?: AddressFamily
        ) => void
      ) => void)
    | ((
        hostname: string,
        options: object
      ) => Promise<
        [address: LookupAddressEntry | LookupAddressEntry[], family?: AddressFamily] | LookupAddress
      >);
  withXSRFToken?: boolean | ((config: InternalAxiosRequestConfig<D, P>) => boolean | undefined);
  parseReviver?: (this: any, key: string, value: any, context?: { source?: string }) => any;
  fetchOptions?: Omit<RequestInit, 'body' | 'headers' | 'method' | 'signal'> | Record<string, any>;
  httpVersion?: 1 | 2;
  http2Options?: Record<string, any> & {
    sessionTimeout?: number;
  };
  formDataHeaderPolicy?: 'legacy' | 'content-only';
  redact?: string[];
  sensitiveHeaders?: string[];
}

// Alias
export type RawAxiosRequestConfig<D = any, P = any> = AxiosRequestConfig<D, P>;

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
  defaults: Omit<AxiosDefaults, 'headers'> & {
    headers: HeadersDefaults & {
      [key: string]: AxiosHeaderValue;
    };
  };
}

export interface GenericFormData {
  append(name: string, value: any, options?: any): any;
}

export interface GenericHTMLFormElement {
  name: string;
  method: string;
  submit(): void;
}

export function getAdapter(
  adapters: AxiosAdapterConfig | AxiosAdapterConfig[] | undefined
): AxiosAdapter;

export function toFormData(
  sourceObj: object,
  targetFormData?: GenericFormData,
  options?: FormSerializerOptions
): GenericFormData;

export function formToJSON(form: GenericFormData | GenericHTMLFormElement): object;

export function isAxiosError<T = any, D = any, P = any>(
  payload: any
): payload is AxiosError<T, D, P>;

export function spread<T, R>(callback: (...args: T[]) => R): (array: T[]) => R;

export function isCancel<T = any, D = any, P = any>(value: any): value is CanceledError<T, D, P>;

export function all<T>(values: Array<T | Promise<T>>): Promise<T[]>;

export function mergeConfig<D = any, P = any>(
  config1: AxiosRequestConfig<D, P>,
  config2: AxiosRequestConfig<D, P>
): AxiosRequestConfig<D, P>;

export function create(config?: CreateAxiosDefaults): AxiosInstance;

export interface AxiosStatic extends AxiosInstance {
  Cancel: typeof CanceledError;
  CancelToken: CancelTokenStatic;
  Axios: typeof Axios;
  AxiosError: typeof AxiosError;
  HttpStatusCode: typeof HttpStatusCode;
  readonly VERSION: string;
  isCancel: typeof isCancel;
  all: typeof all;
  spread: typeof spread;
  isAxiosError: typeof isAxiosError;
  toFormData: typeof toFormData;
  formToJSON: typeof formToJSON;
  getAdapter: typeof getAdapter;
