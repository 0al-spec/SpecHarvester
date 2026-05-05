// swift-tools-version:5.9
// This package exists only to generate DocC documentation for the SpecHarvester
// Python project. The runtime implementation lives under src/spec_harvester.

import PackageDescription

let package = Package(
    name: "SpecHarvester",
    products: [
        .library(
            name: "SpecHarvester",
            targets: ["SpecHarvester"]
        ),
        .executable(
            name: "SpecHarvester-docs",
            targets: ["SpecHarvester-docs"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-docc-plugin", from: "1.0.0"),
    ],
    targets: [
        .target(
            name: "SpecHarvester",
            path: "Sources/SpecHarvester",
            exclude: []
        ),
        .executableTarget(
            name: "SpecHarvester-docs",
            path: "Sources/SpecHarvester-docs",
            exclude: []
        ),
    ]
)
