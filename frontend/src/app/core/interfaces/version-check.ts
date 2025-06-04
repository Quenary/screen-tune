export interface IVersionCheckResponse {
  latest_release_url?: string;
  update_available?: boolean;
  latest_version?: string;
  error?: string;
}
