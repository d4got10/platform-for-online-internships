/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */


export interface paths {
  "/api/course/": {
    /** Get Courses */
    get: operations["get_courses_api_course__get"];
    /** Create Course */
    post: operations["create_course_api_course__post"];
  };
  "/api/course/{course_id}": {
    /** Get Course */
    get: operations["get_course_api_course__course_id__get"];
    /** Delete Course */
    delete: operations["delete_course_api_course__course_id__delete"];
    /** Patch Course */
    patch: operations["patch_course_api_course__course_id__patch"];
  };
  "/api/auth/token": {
    /** Login For Access Token */
    post: operations["login_for_access_token_api_auth_token_post"];
  };
  "/api/users/me": {
    /** Get Users Me */
    get: operations["get_users_me_api_users_me_get"];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    /** Body_login_for_access_token_api_auth_token_post */
    Body_login_for_access_token_api_auth_token_post: {
      /** Grant Type */
      grant_type?: string;
      /** Username */
      username: string;
      /** Password */
      password: string;
      /**
       * Scope 
       * @default
       */
      scope?: string;
      /** Client Id */
      client_id?: string;
      /** Client Secret */
      client_secret?: string;
    };
    /** Course */
    Course: {
      /** Id */
      id: number;
      /** Name */
      name: string;
    };
    /** CreateCourse */
    CreateCourse: {
      /** Name */
      name: string;
      /** Description */
      description: string;
    };
    /** DeleteCourse */
    DeleteCourse: {
      /** Status */
      status: string;
    };
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: (components["schemas"]["ValidationError"])[];
    };
    /** OneCourse */
    OneCourse: {
      /** Id */
      id: number;
      /** Name */
      name: string;
      /** Description */
      description: string;
    };
    /** PatchCourse */
    PatchCourse: {
      /** Name */
      name?: string;
      /** Description */
      description?: string;
    };
    /** Token */
    Token: {
      /** Access Token */
      access_token: string;
      /** Token Type */
      token_type: string;
    };
    /** User */
    User: {
      /** Email */
      email: string;
      /** First Name */
      first_name: string;
      /** Last Name */
      last_name: string;
      /** Patronymic */
      patronymic: string;
      /** Is Admin */
      is_admin: boolean;
      /** Is Teacher */
      is_teacher: boolean;
    };
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type external = Record<string, never>;

export interface operations {

  /** Get Courses */
  get_courses_api_course__get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": (components["schemas"]["Course"])[];
        };
      };
    };
  };
  /** Create Course */
  create_course_api_course__post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["CreateCourse"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["OneCourse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Course */
  get_course_api_course__course_id__get: {
    parameters: {
      path: {
        course_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["OneCourse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Delete Course */
  delete_course_api_course__course_id__delete: {
    parameters: {
      path: {
        course_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["DeleteCourse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Patch Course */
  patch_course_api_course__course_id__patch: {
    parameters: {
      path: {
        course_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["PatchCourse"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["OneCourse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Login For Access Token */
  login_for_access_token_api_auth_token_post: {
    requestBody: {
      content: {
        "application/x-www-form-urlencoded": components["schemas"]["Body_login_for_access_token_api_auth_token_post"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Token"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Users Me */
  get_users_me_api_users_me_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
    };
  };
}