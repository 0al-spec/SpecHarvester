export interface AxiosProgressEvent {
  loaded: number;
  total?: number;
  progress?: number;
  bytes: number;
  rate?: number;
  estimated?: number;
  upload?: boolean;
  download?: boolean;
  event?: BrowserProgressEvent;
  lengthComputable: boolean;
}

type Milliseconds = number;

type AxiosAdapterName = StringLiteralsOrString<'xhr' | 'http' | 'fetch'>;

type AxiosAdapterConfig = AxiosAdapter | AxiosAdapterName;

export type AddressFamily = 4 | 6 | undefined;

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
