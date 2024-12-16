/**
 * Application config interface
 */
export interface IConfig {
    checkUpdates: boolean;
    launchMinimized: boolean;
    /**
     * Names of display devices for which the settings apply.
     */
    displays: string[];
    /**
     * Applications configs
     */
    applications: {
        [key: string]: IConfigApplication;
    };
}

/**
 * Application config
 */
export interface IConfigApplication {
    brightness: number;
    contrast: number;
    gamma: number;
}