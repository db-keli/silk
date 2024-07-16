import { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";
import Preview from "./Preview";
import ProgressBar from "./ProgressBar";
import { Url } from "url";

export default function Search() {
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [state, setState] = useState(false);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [hoverDownload, setHoverDownload] = useState(false);
  const [completed, setCompleted] = useState(0);
  const [downloadStatus, setDownloadStatus] = useState("");
  const [download, setDownload] = useState(false);
  const [downloadTotalLength, setDownloadTotalLength] = useState(0);
  const [downloadReceivedLength, setDownloadReceivedLength] = useState(0);
  const [stream, setStream] = useState(false);
  const [streamTotalLength, setStreamTotalLength] = useState(0);
  const [streamReceivedLength, setStreamReceivedLength] = useState(0);
  const [username, setUsername] = useState(
    Math.floor(Date.now() / 1000).toString()
  );
  const [data, setData] = useState<{ thumbnailLink: string; title: string }[]>(
    []
  );

  useEffect(() => {
    const websocket = new WebSocket(`ws://${BACKEND_URL}/${username}`);
    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "start-download") {
        setDownloadTotalLength(message.video_count);
        setDownload(true);
        setDownloadStatus(message.message);
      } else if (message.type === "end-download") {
        setDownloadStatus(message.message);
        setDownload(false);
        setDownloadTotalLength(0);
        setStream(true);
      } else if (message.type === "progress-check") {
        console.log("check");
        setDownloadReceivedLength(
          (downloadReceivedLength) => downloadReceivedLength + 1
        );
        setDownloadStatus(message.message);
      }
    };
    return () => {
      websocket.close();
    };
  }, []);
  const [selectedResolution, setSelectedResolution] = useState("360p");

  const handleResolutionChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setSelectedResolution(event.target.value);
    console.log(selectedResolution);
  };

  const getDataOnMouseClick = async () => {
    setPreviewLoading(true);
    const link = document.querySelector("input")?.value;
    try {
      const response = await axios.get(
        `http://${BACKEND_URL}/download-video?url=${link}&resolution=${selectedResolution}`
      );
      const data = response.data.data;
      setData(data);
      console.log(String(data));
    } catch (error) {
      console.error(error);
    } finally {
      setPreviewLoading(false);
    }
  };

  const downloadFile = (chunks: BlobPart[] | undefined) => {
    const blob = new Blob(chunks);
    const url = window.URL.createObjectURL(blob);
    const bloblink = document.createElement("a");
    bloblink.href = url;
    bloblink.setAttribute("download", "video.mp4"); // or use a dynamic name
    document.body.appendChild(bloblink);
    bloblink.click();
    document.body.removeChild(bloblink);
  };
  const downloadOnMouseClick = async () => {
    const link: string | URL = document.querySelector("input")?.value || "";
    const url = new URL(link);
    const path = url.pathname;
    try {
      const backendPath =
        path === "/watch" ? "download-video" : "download-playlist";
      const response = await fetch(`http://${BACKEND_URL}/${backendPath}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: String(link),
          resolution: String(selectedResolution),
          username: username,
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const body = response.body;
      if (!body) {
        throw new Error(
          "ReadableStream is not supported or response body is null"
        );
      }

      const reader = body.getReader();
      const contentLength = response.headers.get("Content-Length");
      const totalLength = contentLength ? parseInt(contentLength, 10) : 0;
      setStreamTotalLength(totalLength);

      let chunks: Uint8Array[] = [];

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }
        if (value) {
          const eof = new Uint8Array([10, 10, 10, 10, 10, 10, 10]);
          if (value.length === eof.length) {
            downloadFile(chunks);
            chunks = [];
            continue;
          }
          chunks.push(value);
          setStreamReceivedLength(
            (streamReceivedLength) => streamReceivedLength + value.length
          );
        }
      }
    } catch (error) {
      console.log(error);
    } finally {
      setStream(false);
      setData([]);
    }
  };

  useEffect(() => {
    console.log(streamReceivedLength / streamTotalLength);
    console.log(`Received ${streamReceivedLength} of ${streamTotalLength}`);
  }, [streamReceivedLength]);

  const complete = (received: number, total: number) => {
    const completePercentage = ((received / total) * 100).toFixed(2);
    if (isNaN(parseFloat(completePercentage))) {
      return 0;
    }
    return parseFloat(completePercentage);
  };
  return (
    <>
      <div className="flex flex-row mt-20">
        <div className="basis-1/12" />
        <input
          name="Search"
          type="text"
          maxLength={90}
          className="basis-9/12 border-white"
          placeholder="  Paste Link Here"
        />
        <div
          onMouseEnter={() => setState(true)}
          onMouseLeave={() => setState(false)}
          className={
            state === true
              ? "ml-2 basis-1/12 rounded-md"
              : "ml-2 basis-1/12 rounded-md"
          }
        >
          <button
            className={
              state === true
                ? "font-open text-white underline"
                : "font-open text-white"
            }
            onClick={getDataOnMouseClick}
          >
            Submit
          </button>
        </div>
        <div className="basis-1/12" />
      </div>
      {previewLoading && (
        <div className=" justify-center text-center mt-2 font-open text-white loader">
          <div className=" justify-center text-center mt-2 font-open text-white loader">
            Loading......
          </div>
        </div>
      )}
      <div>
        {previewLoading === false && data.length > 0 && (
          <Preview thumbnailLink={String(data[1])} title={String(data[0])} />
        )}
      </div>
      <div>
        {download && (
          <div className=" justify-center text-center mt-2 font-open text-white loader">
            <ProgressBar
              completed={complete(downloadReceivedLength, downloadTotalLength)}
            />
            <div className=" justify-center text-center mt-2 font-open text-white loader">
              {downloadStatus}
            </div>
          </div>
        )}
      </div>
      <div>
        {stream && (
          <div className=" justify-center text-center mt-2 font-open text-white loader">
            <ProgressBar
              completed={complete(streamReceivedLength, streamTotalLength)}
            />
          </div>
        )}
      </div>
      <div className="flex flex-row mt-20">
        <div className="basis-1/12" />
        <button
          className={
            hoverDownload === true
              ? "basis-7/12 bg-cyan-600 rounded-md font-open text-white font-bold text-center w-full"
              : "basis-7/12 bg-cyan-600 rounded-md font-open text-white text-center w-full"
          }
          onMouseEnter={() => setHoverDownload(true)}
          onMouseLeave={() => setHoverDownload(false)}
          onClick={() => downloadOnMouseClick()}
        >
          download
        </button>
        <div className="basis-3/12">
          <select
            id="resolutions"
            value={selectedResolution}
            onChange={handleResolutionChange}
            className="ml-3 col-span-3 block w-full"
          >
            <option value="">Select a resolution</option>
            <option value="1080p">1080p</option>
            <option value="720p">720p</option>
            <option value="480p">480p</option>
            <option value="360p">360p</option>
            <option value="240p">240p</option>
            <option value="144p">144p</option>
          </select>
        </div>
      </div>
    </>
  );
}
