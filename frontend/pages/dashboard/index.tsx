import Layout from "@/components/Layout";
import {useSession} from "next-auth/react";
import {useEffect, useState} from "react";
import Link from "next/link";
import ChipStatus from "@/components/dashboard/StatusChip";
import {Button} from "@nextui-org/react";


async function getListInputData(access_token: string) {
	const res = await fetch(process.env.API_URL + "ai/input/", {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function getInputDataDetails(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/input/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}

async function getListResult(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/result/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function postResponse(access_token: string, inputDataId: string, result_type: string){
	const res = await fetch(process.env.API_URL + "ai/result/", {
		method: "post",
		headers: {
			Authorization: `Bearer ${access_token}`,
		 'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify({
			input_id: inputDataId,
			result_type: result_type
		})
	})
	return await res.json();
}


const resultType: String[] = ["NOTE", "SUMMARY"];


export default function Dashboard() {
	const {data: session, status} = useSession({required: true});

	const [listInputData, setListInputData] = useState([]);
	const [detailInputData, setDetailInputData] = useState(null);
	const [listResult, setListResult] = useState([]);
	const [isLoading, setIsLoading] = useState(false);


	useEffect(() => {
		async function fetchData() {
			const data = await getListInputData(session?.access_token);
			setListInputData(data);
		}

		fetchData();
	}, [session?.access_token]);

	const handleListItemClick = async (inputDataId) => {
    const detailInputData = await getInputDataDetails(session?.access_token, inputDataId);
		setDetailInputData(detailInputData);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);
  };

	const handleResponseCreate = async (inputDataId, resultType) => {
		setIsLoading(true);
		const response = await postResponse(session?.access_token, inputDataId, resultType);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);

		setIsLoading(false);
	}

	return (
		<>
			<Layout>
				<main>
					{
						<>
							<button data-drawer-target="default-sidebar" data-drawer-toggle="default-sidebar"
											aria-controls="default-sidebar" type="button"
											className="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
								<span className="sr-only">Open sidebar</span>
								<svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"
										 xmlns="http://www.w3.org/2000/svg">
									<path clip-rule="evenodd" fill-rule="evenodd"
												d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
								</svg>
							</button>

							<aside id="default-sidebar"
										 className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
										 aria-label="Sidebar">
								<div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
									<ul className="space-y-2 font-medium">

										{Array.isArray(listInputData) && (
											listInputData.map((inputData) => (
												<li key={inputData?.id}>

													<Link href="#" onClick={() => handleListItemClick(inputData?.id)}>
														<div>
															<span className="flex-1 truncate">{inputData?.source_title}</span>
															<ChipStatus status={inputData?.status}/>
														</div>
													</Link>
												</li>
											))
										)}

									</ul>
								</div>
							</aside>

							<div className="p-4 sm:ml-64 flex flex-wrap">
								<div
									className="p-4 w-1/2 border-2 border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
									style={{maxHeight: "850px"}}>
									{detailInputData?.fragments.length > 0 && (
										detailInputData?.fragments.map((detail) => (
											<li key={detail?.id} className={"mb-5"}>
												<div>
													<strong>
														{detail.start_time.hours}:{detail.start_time.minutes}:{detail.start_time.seconds}
													</strong>
													-
													<strong>
														{detail.end_time.hours}:{detail.end_time.minutes}:{detail.end_time.seconds}
													</strong>
													<p>{detail?.text}</p>
												</div>
											</li>
										))
									)}
								</div>
								<div
									className="p-4 w-1/2 border-2 border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
									style={{maxHeight: "850px"}}>
									{Array.isArray(listResult) && (listResult.length> 0 && (
										listResult?.map((result) => (
											<li key={result?.id} className={"mb-5"}>
												<div>
													<strong>{result?.result_type}</strong>
													<p>{result?.content}</p>
												</div>
											</li>
										))
									))}
								</div>

							{resultType.map((resultType, index) => (
								<div key={index}>
									<Button isLoading={isLoading} type={"button"} onClick={() => handleResponseCreate(detailInputData?.id, resultType)}>
											{resultType}
									</Button>
								</div>
            	))}
							</div>



						</>
					}
				</main>
			</Layout>
		</>
	);
}