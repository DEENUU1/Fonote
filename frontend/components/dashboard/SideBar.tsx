
import Link from "next/link";
import ChipStatus from "@/components/dashboard/StatusChip";
import {useState} from "react";
import CreateInputModal from "@/components/dashboard/CreateInputModal";
import SidebarButton from "@/components/dashboard/SidebarButton";


export default function SideBar(
	{
		listInputData,
		handleListItemClick,
		handleSubmitCreateInputData,
		setUrl,
		setLanguage,
		setTranscription
	}:
	{
		listInputData: any[],
		handleListItemClick: (id: string) => void,
		handleSubmitCreateInputData: (data: any) => void,
		setUrl: (url: string) => void,
		setLanguage: (language: string) => void,
		setTranscription: (transcription: string) => void
	}

){
	const [sidebarIsOpen, setSideBarIsOpen] = useState(false);

	const toggleSidebar = () => {
		setSideBarIsOpen(!sidebarIsOpen);
	};


	return (
		<>
			<SidebarButton toggleSidebar={toggleSidebar}/>

			<aside
				id="default-sidebar"
				className={`fixed top-0 left-0 z-40 w-64 h-screen transition-transform ${
					sidebarIsOpen ? '' : '-translate-x-full'
				} sm:translate-x-0`}
				aria-label="Sidebar"
			>
				<div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
					<button
						onClick={toggleSidebar}
						className="absolute top-0 right-0 p-2 text-gray-500 hover:text-gray-600 focus:outline-none"
					>
						<span className="sr-only">Close sidebar</span>
						<svg
							className="w-6 h-6"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth={2}
								d="M6 18L18 6M6 6l12 12"
							/>
						</svg>
					</button>
					<ul className="space-y-2 font-medium">

						<CreateInputModal
							handleSubmitCreateInputData={handleSubmitCreateInputData}
							setUrl={setUrl}
							setLanguage={setLanguage}
							setTranscription={setTranscription}
						/>


						{Array.isArray(listInputData) && (
							listInputData.map((inputData) => (
								<li className={"hover:bg-gray-200 rounded-xl p-2 overflow-hidden overflow-ellipsis"}
										key={inputData?.id}>
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

		</>
	)
}