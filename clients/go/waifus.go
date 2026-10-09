package waifus

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

const DefaultBaseURL = "https://wafus.vercel.app"

type Client struct {
	BaseURL    string
	APIKey     string
	HTTPClient *http.Client
}

type Waifu struct {
	ID              string `json:"id,omitempty"`
	WaifuID         string `json:"waifu_id,omitempty"`
	Name            string `json:"name"`
	Rarity          string `json:"rarity"`
	EventTag        string `json:"event_tag"`
	ImgURL          string `json:"img_url"`
	SourceMessageID int    `json:"source_message_id,omitempty"`
	OriginalChannel string `json:"original_channel,omitempty"`
	AddedBy         string `json:"added_by,omitempty"`
}

type RandomResponse struct {
	Status string `json:"status"`
	Data   Waifu  `json:"data"`
}

type ListResponse struct {
	Status  string  `json:"status"`
	Showing int     `json:"showing"`
	Skip    int     `json:"skip"`
	Limit   int     `json:"limit"`
	Data    []Waifu `json:"data"`
}

type StatsResponse struct {
	Status       string `json:"status"`
	TotalRecords int    `json:"total_records"`
	Database     string `json:"database"`
}

func NewClient(apiKey string) *Client {
	return &Client{
		BaseURL: DefaultBaseURL,
		APIKey:  apiKey,
		HTTPClient: &http.Client{
			Timeout: 15 * time.Second,
		},
	}
}

func (c *Client) do(ctx context.Context, method, path string, body any, out any) error {
	reqURL := strings.TrimRight(c.BaseURL, "/") + path

	var bodyReader io.Reader
	if body != nil {
		data, err := json.Marshal(body)
		if err != nil {
			return err
		}
		bodyReader = bytes.NewReader(data)
	}

	req, err := http.NewRequestWithContext(ctx, method, reqURL, bodyReader)
	if err != nil {
		return err
	}

	req.Header.Set("Accept", "application/json")
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	if c.APIKey != "" {
		req.Header.Set("x-api-key", c.APIKey)
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		b, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("api error (%d): %s", resp.StatusCode, string(b))
	}

	if out != nil {
		return json.NewDecoder(resp.Body).Decode(out)
	}
	return nil
}

func (c *Client) Random(ctx context.Context) (*Waifu, error) {
	var resp RandomResponse
	err := c.do(ctx, http.MethodGet, "/Random", nil, &resp)
	if err != nil {
		return nil, err
	}
	return &resp.Data, nil
}

func (c *Client) Stats(ctx context.Context) (*StatsResponse, error) {
	var resp StatsResponse
	err := c.do(ctx, http.MethodGet, "/Stats", nil, &resp)
	return &resp, err
}

func (c *Client) List(ctx context.Context, skip, limit int) (*ListResponse, error) {
	var resp ListResponse
	path := fmt.Sprintf("/List?skip=%d&limit=%d", skip, limit)
	err := c.do(ctx, http.MethodGet, path, nil, &resp)
	return &resp, err
}

func (c *Client) FindByName(ctx context.Context, name string) (*RandomResponse, error) {
	var resp RandomResponse
	path := fmt.Sprintf("/Find?name=%s", url.QueryEscape(name))
	err := c.do(ctx, http.MethodGet, path, nil, &resp)
	return &resp, err
}
