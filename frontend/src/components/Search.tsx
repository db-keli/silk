import { useState, ChangeEvent } from "react";
import axios from "axios";
import Preview from "./Preview";

export default function Search() {
  const [state, setState] = useState(false);
  const [loading, setLoading] = useState(false);
  const [hoverDownload, setHoverDownload] = useState(false);
  const [data, setData] = useState<{ thumbnailLink: string; title: string }[]>(
    []
  );
  const [selectedResolution, setSelectedResolution] = useState("360p");

  const handleResolutionChange = (event: ChangeEvent<HTMLSelectElement>) => {
    setSelectedResolution(event.target.value);
    console.log(selectedResolution);
  };
  const getData = async (event: ChangeEvent) => {
    setLoading(true);
    const link = (event.target as HTMLInputElement).value;
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/download-video/?url=${link}&resolution=${selectedResolution}`
      );
      const data = response.data.data;
      setData(data);
      console.log(String(data));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getDataOnMouseClick = async () => {
    setLoading(true);
    const link = document.querySelector("input")?.value;
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/download-video/?url=${link}&resolution=${selectedResolution}`
      );
      const data = response.data.data;
      setData(data);
      console.log(String(data));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const [download, setDownload] = useState(false);
  const downloadOnMouseClick = async () => {
    setDownload(true);
    const link = document.querySelector("input")?.value;
    try {
      const response = await axios.post(
        "/http://127.0.0.1:8000/download-video",
        { url: link, resolution: selectedResolution }
      );
      return response;
    } catch (error) {
      console.log(error);
    } finally {
      setDownload(false);
    }
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
          onChange={(event) => getData(event)}
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
      {loading && (
        <div className=" justify-center text-center mt-2 font-open text-white loader">
          Loading......
        </div>
      )}
      <div>
        {loading === false && data.length > 0 && (
          <Preview thumbnailLink={String(data[1])} title={String(data[0])} />
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
          onClick={() => downloadOnMouseClick}
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
